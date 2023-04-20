from dolfin import *
set_log_level(50)

comm = MPI.comm_world
rank = MPI.rank(comm)


def mprint(*argv):
    if rank == 0:
        out = ""
        for arg in argv:
            out = out + str(arg)
        # this forces program to output when run in parallel
        print(out, flush=True)

def epsilon(v):
    return sym(grad(v))

def sigma(v):
    return lmbda*tr(epsilon(v))*Identity(2) + 2.0*mu*epsilon(v)


lx, ly, mul = 10, 1, 3
nx, ny = int(lx * mul), int(ly * mul)
mesh = RectangleMesh(comm, Point(0., 0.), Point(lx, ly), nx, ny, "crossed")

E, nu, rho = Constant(2e11), Constant(0.3), Constant(7850) # E=N/m2 and rho=kg/m3
mu, lmbda = E/2/(1+nu), E*nu/(1+nu)/(1-2*nu)
lmbda = 2*mu*lmbda/(lmbda+2*mu)

rho_g = rho * 9.8 * 100
f = Constant((0, -rho_g))
U = VectorFunctionSpace(mesh, 'Lagrange', degree=1)
u, v = TrialFunction(U), TestFunction(U)
a = inner(sigma(u), epsilon(v))*dx
l = inner(f, v)*dx

mprint("DoF: ", (U.dim()))

left = CompiledSubDomain("near(x[0], 0.0, tol) && on_boundary", tol=1e-14)

bc = DirichletBC(U, Constant((0., 0.)), left)
u_sol = Function(U, name="displacement")
problem = LinearVariationalProblem(a, l, u_sol, bc)
solver = LinearVariationalSolver(problem)

prm = solver.parameters
prm["linear_solver"] = 'cg'
prm["preconditioner"] = 'hypre_euclid'
solver.solve()

mprint("Maximal deflection    : ", -
       round(MPI.min(comm, u_sol.vector().min()), 3))
mprint("Beam theory deflection: ", round(3*rho_g*lx**4/2/E/ly**3, 3))

file_results = XDMFFile(comm, "output/elasticity_results.xdmf")
file_results.parameters["flush_output"] = True
file_results.parameters["functions_share_mesh"] = True
file_results.write(u_sol)

solvers = (
    "bicgstab",
    "cg",
    "default",
    "gmres",
    "minres",
    "mumps",
    "petsc",
    "richardson",
    "superlu",
    "tfqmr",
    "umfpack",
)

preconditioners = (
    "amg",
    "default",
    "hypre_amg",
    "hypre_euclid",
    "hypre_parasails",
    "icc",
    "ilu",
    "jacobi",
    "none",
    "petsc_amg",
    "sor",
)

linesearch = ("basic", "bt", "cp", "l2", "nleqerr")

# list_timings(TimingClear.clear, [TimingType.wall])

