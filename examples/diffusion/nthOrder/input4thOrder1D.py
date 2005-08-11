#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 8/10/05 {3:13:11 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

r"""

This example uses the `ImplicitDiffusionTerm` class to solve the equation

.. raw:: latex

    $$ \frac{\partial^4 \phi}{\partial x^4} = 0 $$

on a 1D mesh of length

    >>> L = 1000.
    
We create an appropriate mesh

    >>> nx = 1000
    >>> dx = L / nx
    >>> from fipy.meshes.grid1D import Grid1D
    >>> mesh = Grid1D(dx = dx, nx = nx)

and initialize the solution variable to 0

    >>> from fipy.variables.cellVariable import CellVariable
    >>> var = CellVariable(
    ...     name = "concentration",
    ...     mesh = mesh,
    ...     value = 0.)
    
For this problem, we impose the boundary conditions:

.. raw:: latex

    \begin{alignat*}{2}
    \phi &= \alpha_1 &\quad& \text{at $x = 0$} \\
    \frac{\partial \phi}{\partial x} &= \alpha_2 && \text{at $x = L$} \\
    \frac{\partial^2 \phi}{\partial x^2} &= \alpha_3 && \text{at $x = 0$} \\
    \frac{\partial^3 \phi}{\partial x^3} &= \alpha_4 && \text{at $x = L$.}
    \end{alignat*}
    
or

    >>> alpha1 = 2.
    >>> alpha2 = 1.
    >>> alpha3 = 4.
    >>> alpha4 = -3.
    
    >>> from fipy.boundaryConditions.fixedValue import FixedValue
    >>> from fipy.boundaryConditions.fixedFlux import FixedFlux
    >>> from fipy.boundaryConditions.nthOrderBoundaryCondition \
    ...     import NthOrderBoundaryCondition
    >>> BCs = (FixedValue(mesh.getFacesLeft(), alpha1),
    ...        FixedFlux(mesh.getFacesRight(), alpha2),
    ...        NthOrderBoundaryCondition(mesh.getFacesLeft(), alpha3, 2),
    ...        NthOrderBoundaryCondition(mesh.getFacesRight(), alpha4, 3))

We initialize the steady-state equation and use the `LinearLUSolver` for stability. 

    >>> from fipy.solvers.linearLUSolver import LinearLUSolver

We perform one implicit timestep to achieve steady state
    
    >>> from fipy.terms.implicitDiffusionTerm import ImplicitDiffusionTerm
    >>> eq = ImplicitDiffusionTerm(coeff = (1, 1)) == 0
    >>> eq.solve(var,
    ...          boundaryConditions = BCs,
    ...          solver = LinearLUSolver(tolerance = 1e-11))

The analytical solution is:

.. raw:: latex

   $$ \phi = \frac{ \alpha_4 }{6} x^3 + \frac{ \alpha_3 }{2} x^2 
   + \left( \alpha_2 - \frac{ \alpha_4 }{2} L^2  - \alpha_3 L \right) x + \alpha_1 $$

or

    >>> x = mesh.getCellCenters()[:,0]
    >>> answer = alpha4 / 6. * x**3 + alpha3 / 2. * x**2 
    >>> answer += (alpha2 - alpha4 / 2. * L**2 - alpha3 * L) * x + alpha1
    >>> print var.allclose(answer, rtol = 1e-4)
    1

If the problem is run interactively, we can view the result:
    
    >>> if __name__ == '__main__':
    ...     import fipy.viewers
    ...     viewer = fipy.viewers.make(vars = var)
    ...     viewer.plot()

"""
__docformat__ = 'restructuredtext'

## from fipy.solvers.linearPCGSolver import LinearPCGSolver

if __name__ == '__main__':
    import fipy.tests.doctestPlus
    exec(fipy.tests.doctestPlus._getScript())
    raw_input('finished')
