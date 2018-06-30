from vtk import vtkPolyData, vtkFloatArray, vtkPoints, vtkIdTypeArray
from vtk import vtkCellArray, vtkIntArray, vtkSmoothPolyDataFilter, vtkPolyDataNormals
import numpy as np

def gii2polydata(mesh, smooth=False, normals=False):
    """ Convert a Gifti mesh to vtk polydata
        This function converts a Gifti mesh into a VTK polydata.

        :param gii: Gifti mesh
        :type gii: 'nibabel.gifti.gifti.GiftiImage'
        :param smooth: falg to smooth mesh
        :type smooth: bool
        :param normals: flag to compute normals
        :type normals: bool
        :return: vtk mesh
        :rtype: vtk.vtkPolydata
    """
    for da in mesh.darrays:
        if da.intent == 1008:  # nib.nifti1.intent_codes.NIFTI_INTENT_POINTSET
            # Create vtk array from nib data
            points_data = vtkFloatArray()
            points_data.SetNumberOfComponents(3)
            points_data.SetArray(da.data, da.data.shape[0] * 3, 1)

            # Set vtk array as points
            points = vtkPoints()
            points.SetData(points_data)

        elif da.intent == 1009:  # nib.nifti1.intent_codes.NIFTI_INTENT_TRIANGLE
            # To represent triangles, cells need to be [num_idxs, idx0, idx1, idx2], with num_idxs = 3
            triangles_array = np.hstack([np.ones((da.data.shape[0], 1)) * 3, np.array(da.data)]).astype(np.longlong, copy=False)
            # Create vtk array from nib data
            triangles_data = vtkIdTypeArray()
            triangles_data.SetNumberOfComponents(4)
            triangles_data.SetArray(triangles_array, da.data.shape[0] * 4, 1)

            # Set vtk array as cells (triangles)
            triangles = vtkCellArray()
            triangles.SetCells(da.data.shape[0], triangles_data)

    polydata = vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetPolys(triangles)

    if smooth:
        smoothFilter = vtkSmoothPolyDataFilter()
        smoothFilter.SetInputData(polydata)
        smoothFilter.SetNumberOfIterations(15)
        smoothFilter.SetRelaxationFactor(0.1)
        smoothFilter.FeatureEdgeSmoothingOn()
        smoothFilter.BoundarySmoothingOff()
        smoothFilter.Update()
        polydata = smoothFilter.GetOutput()

    if normals:
        normalGenerator = vtkPolyDataNormals()
        normalGenerator.ComputePointNormalsOn()
        normalGenerator.ComputeCellNormalsOn()
        normalGenerator.SetInputData(polydata)
        normalGenerator.AutoOrientNormalsOn()
        normalGenerator.Update()
        polydata = normalGenerator.GetOutput()

    return polydata
