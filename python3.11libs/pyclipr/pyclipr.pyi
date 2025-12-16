import enum
from typing import Annotated

from numpy.typing import ArrayLike


clipperVersion: str = '1.5.4'

class PolyPath:
    @property
    def level(self) -> int: ...

    @property
    def parent(self) -> PolyPath: ...

class PolyTree:
    @property
    def isHole(self) -> bool: ...

    @property
    def area(self) -> float: ...

    @property
    def attributes(self) -> object: ...

    @property
    def polygon(self) -> object: ...

    @property
    def children(self) -> "std::vector<Clipper2Lib::PolyPath64 const * __ptr64,std::allocator<Clipper2Lib::PolyPath64 const * __ptr64> >": ...

    @property
    def count(self) -> int: ...

    def __len__(self) -> int: ...

class PolyTreeD:
    @property
    def isHole(self) -> bool: ...

    @property
    def area(self) -> float: ...

    @property
    def attributes(self) -> object: ...

    @property
    def polygon(self) -> object: ...

    @property
    def children(self) -> "std::vector<Clipper2Lib::PolyPathD const * __ptr64,std::allocator<Clipper2Lib::PolyPathD const * __ptr64> >": ...

    @property
    def count(self) -> int: ...

    def __len__(self) -> int: ...

def polyTreeToPaths64(arg0: PolyTree, arg1: float, /) -> object: ...

def orientation(path: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F', device='cpu')], scaleFactor: float = 1000) -> bool:
    """
    This function returns the orientation of a path. Orientation will return `True` if the polygon's orientation
    is counter-clockwise.

    :param path: A 2D numpy array of shape (n, 2) or (n, 3) where n is the number of vertices in the path.
    :param scaleFactor: Optional scale factor for the internal clipping factor. Defaults to 1000.
    :return: `True` if the polygon's orientation is counter-clockwise, `False` otherwise.
    """

def polyTreeToPaths(arg0: PolyTree, arg1: float, /) -> object: ...

def simplifyPath(path: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F', device='cpu')], epsilon: float, scaleFactor: float, isOpenPath: bool = False) -> object:
    """
    This function removes vertices that are less than the specified epsilon distance from an imaginary line
    that passes through its two adjacent vertices. Logically, smaller epsilon values will be less aggressive
    in removing vertices than larger epsilon values.

    :param path: A 2D numpy array of shape (n, 2) or (n, 3) where n is the number of vertices in the path.
    :param epsilon: The maximum distance a vertex can be from an imaginary line that passes through its two adjacent vertices.
    :param scaleFactor: The scaleFactor applied to the path during simplification
    :param isOpenPath: If `True`, the path is treated as an open path. If `False`, the path is treated as a closed path.
    :return: Simplified path
    """

def simplifyPaths(paths: "std::vector<ndarray<double,numpy,detail::shape<-1,-1>,device::cpu,f_contig>,std::allocator<ndarray<double,numpy,detail::shape<-1,-1>,device::cpu,f_contig> > >", epsilon: float, scaleFactor: float, isOpenPath: bool = False) -> object:
    """
    This function removes vertices that are less than the specified epsilon distance from an imaginary line
    that passes through its two adjacent vertices. Logically, smaller epsilon values will be less aggressive
    in removing vertices than larger epsilon values.

    :param paths: A list of 2D points (x,y) that define the path. Tuple or a numpy array may be provided for the path
    :param epsilon: The maximum distance a vertex can be from an imaginary line that passes through its 2 adjacent vertices.
    :param scaleFactor: The scaleFactor applied to the path during simplification
    :param isOpenPath: If `True`, the path is treated as an open path. If `False`, the path is treated as a closed path.
    :return: None
    """

class Clipper:
    """
    The Clipper class manages the process of clipping polygons using a number of different Boolean operations,
    by providing a list of open or closed subject and clipping paths. These are internally represented with Int64
    precision, that requires the user to specify a scaleFactor.
    """

    def __init__(self) -> None: ...

    @property
    def scaleFactor(self) -> float:
        """
        The scale factor to be for transforming the input and output vectors. The default is 1000.
        """

    @scaleFactor.setter
    def scaleFactor(self, arg: float, /) -> None: ...

    @property
    def preserveCollinear(self) -> bool:
        """
        By default, when three or more vertices are collinear in input polygons (subject or clip),
        the Clipper object removes the 'inner' vertices before clipping. When enabled the PreserveCollinear property
        prevents this default behavior to allow these inner vertices to appear in the solution.
        """

    @preserveCollinear.setter
    def preserveCollinear(self, arg: bool, /) -> None: ...

    def addPath(self, path: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F', device='cpu')], pathType: PathType, isOpen: bool = False) -> None:
        """
        The addPath method adds one or more closed subject paths (polygons) to the Clipper object.

        :param path: A list of 2D points (x,y) that define the path. Tuple or a numpy array may be provided
        :param pathType: A PathType enum value that indicates whether the path is a subject or a clip path.
        :param isOpen: A boolean value that indicates whether the path is closed or not. Default is 'False'
        :return: None
        """

    def addPaths(self, paths: "std::vector<ndarray<double,numpy,detail::shape<-1,-1>,device::cpu,f_contig>,std::allocator<ndarray<double,numpy,detail::shape<-1,-1>,device::cpu,f_contig> > >", pathType: PathType, isOpen: bool = False) -> None:
        """
        The AddPath method adds one or more closed subject paths (polygons) to the Clipper object.

        :param path: A list paths, each consisting 2D points (x,y) that define the path. A Tuple or a numpy array may be provided
        :param pathType: A PathType enum value that indicates whether the path is a subject or a clip path.
        :param isOpen: A boolean value that indicates whether the path is closed or not. Default is `False`
        :param returnZ: If `True`, returns a separate array of the Z attributes for clipped paths. Default is `False`
        :return: None
        """

    def execute(self, clipType: ClipType, fillRule: FillRule, *, returnOpenPaths: bool = False, returnZ: bool = False) -> object:
        """
        The execute method performs the Boolean clipping operation on the polygons or paths that have been added
        to the clipper object. This method will return a list of paths from the result. The default fillRule is
        even-odd typically used for the representation of polygons.

        :param clipType: The ClipType or the clipping operation to be used for the paths
        :param fillRule: A FillType enum value that indicates the fill representation for the paths
        :param returnOpenPaths: If `True`, returns a tuple consisting of both open and closed paths
        :param returnZ: If `True`, returns a separate array of the Z attributes for clipped paths. Default is `False`
        :return: A resultant paths that have been clipped
        """

    def execute2(self, clipType: ClipType, fillRule: FillRule, *, returnOpenPaths: bool = False, returnZ: bool = False) -> object:
        """
        The execute2 method performs the Boolean clipping operation on the polygons or paths that have been added
        to the clipper object. TThis method will return a PolyTree of the result structuring the output into the hierarchy of
        the paths that form the exterior and interior polygon.

        The default fillRule is even-odd typically used for the representation of polygons.

        :param clipType: The ClipType or the clipping operation to be used for the paths
        :param fillRule: A FillType enum value that indicates the fill representation for the paths
        :param returnOpenPaths: If `True`, returns a tuple consisting of both open and closed paths. Default is `False`
        :param returnZ: If `True`, returns a separate array of the Z attributes for clipped paths. Default is `False`
        :return: A resultant polytree of the clipped paths
        """

    def executeTree(self, clipType: ClipType, fillRule: FillRule, *, returnOpenPaths: bool = False, returnZ: bool = False) -> object:
        """
        The `executeTree` method performs the Boolean clipping operation on the polygons or paths that have been added
        to the clipper object. TThis method will return a PolyTree of the result structuring the output into the hierarchy of
        the paths that form the exterior and interior polygon.

        The default `FillRule` is even-odd typically used for the representation of polygons.

        :param clipType: The ClipType or the clipping operation to be used for the paths
        :param fillRule: A FillType enum value that indicates the fill representation for the paths
        :param returnOpenPaths: If `True`, returns a tuple consisting of both open and closed paths. Default is `False`
        :param returnZ: If `True`, returns a separate array of the Z attributes for clipped paths. Default is `False`
        :return: A resultant paths that have been clipped
        """

    def clear(self) -> None:
        """The clear method removes all the paths from the Clipper object."""

    def cleanUp(self) -> None: ...

class PathType(enum.Enum):
    """The path type"""

    Subject = 0
    """The subject path"""

    Clip = 1
    """The clipping path"""

Subject: PathType = PathType.Subject

Clip: PathType = PathType.Clip

class ClipType(enum.IntEnum):
    """The clipping operation type"""

    Union = 2
    """Union operation"""

    Difference = 3
    """Difference operation"""

    Intersection = 1
    """Intersection operation"""

    Xor = 4
    """XOR operation"""

Union: ClipType = ClipType.Union

Difference: ClipType = ClipType.Difference

Intersection: ClipType = ClipType.Intersection

Xor: ClipType = ClipType.Xor

class FillRule(enum.IntEnum):
    """The fill rule to be used for the clipping operation"""

    EvenOdd = 0
    """Even and Odd Fill"""

    NonZero = 1
    """Non-Zero Fill"""

    Positive = 2
    """Positive Fill"""

    Negative = 3
    """Negative Fill"""

class ClipperOffset:
    """
    The ClipperOffset class manages the process of offsetting  (inflating/deflating)
    both open and closed paths using a number of different join types and end types.
    The library user will rarely need to access this unit directly since it will generally
    be easier to use the InflatePaths function when doing polygon offsetting.
    """

    def __init__(self) -> None: ...

    @property
    def scaleFactor(self) -> float:
        """
        Scale factor for transforming the input and output vectors. The default is 1000.
        """

    @scaleFactor.setter
    def scaleFactor(self, arg: float, /) -> None: ...

    @property
    def arcTolerance(self) -> float:
        """
        Firstly, this field/property is only relevant when JoinType = Round and/or EndType = Round.

        Since flattened paths can never perfectly represent arcs, this field/property specifies a maximum acceptable
        imprecision ('tolerance') when arcs are approximated in an offsetting operation. Smaller values will increase
        'smoothness' up to a point though at a cost of performance and in creating more vertices to construct the arc.

        The default ArcTolerance is 0.25 units. This means that the maximum distance the flattened path will deviate
        from the 'true' arc will be no more than 0.25 units (before rounding).
        """

    @arcTolerance.setter
    def arcTolerance(self, arg: float, /) -> None: ...

    @property
    def miterLimit(self) -> float:
        """
        This property sets the maximum distance in multiples of delta that vertices can be offset from their original
        positions before squaring is applied. (Squaring truncates a miter by 'cutting it off' at 1 x delta distance
        from the original vertex.)

        The default value for MiterLimit is 2 (ie twice delta).
        """

    @miterLimit.setter
    def miterLimit(self, arg: float, /) -> None: ...

    @property
    def preserveCollinear(self) -> bool:
        """
        By default, when three or more vertices are collinear in input polygons (subject or clip),
        the Clipper object removes the 'inner' vertices before clipping. When enabled the `PreserveCollinear` property
        prevents this default behavior to allow these inner vertices to appear in the solution.
        """

    @preserveCollinear.setter
    def preserveCollinear(self, arg: bool, /) -> None: ...

    def addPath(self, path: Annotated[ArrayLike, dict(dtype='float64', shape=(None, None), order='F', device='cpu')], joinType: JoinType, endType: EndType) -> None:
        """
        The addPath method adds one open or closed paths (polygon) to the ClipperOffset object.

        :param path: A list of 2D points (x,y) that define the path. Tuple or a numpy array may be provided for the path
        :param joinType: The JoinType to use for the offsetting / inflation of paths
        :param endType: The EndType to use for the offsetting / inflation of paths (default is Polygon)
        :return: None
        """

    def addPaths(self, path: "std::vector<ndarray<double,numpy,detail::shape<-1,-1>,device::cpu,f_contig>,std::allocator<ndarray<double,numpy,detail::shape<-1,-1>,device::cpu,f_contig> > >", joinType: JoinType, endType: EndType) -> None:
        """
        The addPath method adds one or more open / closed paths to the ClipperOffset object.

        :param path: A list of paths consisting of 2D points (x,y) that define the path. Tuple or a numpy array may be provided for each path
        :param joinType: The JoinType to use for the offsetting / inflation of paths
        :param endType: The EndType to use for the offsetting / inflation of paths
        :return: None
        """

    def execute(self, delta: float) -> object:
        """
        The `execute` method performs the offsetting/inflation operation on the polygons or paths that have been added
        to the clipper object. This method will return a list of paths from the result.

        :param delta: The offset to apply to the inflation/offsetting of paths and segments
        :return: The resultant offset paths
        """

    def execute2(self, delta: float) -> PolyTreeD:
        """
        The `execute` method performs the offsetting/inflation operation on the polygons or paths that have been added
        to the clipper object. This method will return a PolyTree from the result, that considers the hierarchy of the interior and exterior
        paths of the polygon.

        :param delta: The offset to apply to the inflation/offsetting
        :return: A resultant offset paths created in a PolyTree64 Object
        """

    def executeTree(self, delta: float) -> PolyTreeD:
        """
        The `executeTree` method performs the offsetting/inflation operation on the polygons or paths that have been added
        to the clipper object. This method will return a PolyTree from the result, that considers the hierarchy of the interior and exterior
        paths of the polygon.

        :param delta: The offset to apply to the inflation/offsetting
        :return: A resultant offset paths created in a PolyTree64 Object
        """

    def clear(self) -> None:
        """The clear method removes all the paths from the ClipperOffset object."""

class JoinType(enum.IntEnum):
    """The join type to be used for the offsetting / inflation of paths"""

    Square = 0
    """Square join type"""

    Round = 2
    """Round join type"""

    Miter = 3
    """Miter join type"""

class EndType(enum.IntEnum):
    """The end type to be used for the offsetting / inflation of paths"""

    Square = 3
    """Square end type"""

    Butt = 2
    """Butt end type"""

    Joined = 1
    """Joined end type"""

    Polygon = 0
    """Polygon end type"""

    Round = 4
    """Round end type"""
