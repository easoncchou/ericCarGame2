class PhysicsObject:
    """
    Any rectangular object with physics
    """

    def __init__(self, mass: int, moi: int,
                 size: tuple[int, int], pivot: tuple[int, int]) -> None:
        """
        Initializer
        """

        self.mass = mass
        self.moi = moi          # moment of inertia
        self.size = size
        self.pivot = pivot      # pivot point for the car

        self.pos = (0, 0)       # (x, y)
        self.vel = (0, 0)       # (norm, tan)
        self.acc = (0, 0)       # (norm, tan)

        self.a_pos = 0          # angular position
        self.a_vel = 0          # angular velocity
        self.a_acc = 0          # angular acceleration

    def apply_force(self, pos: tuple[int, int]) -> None:
        """
        Applies a force relative to this PhysicsObject
        :return:
        """
