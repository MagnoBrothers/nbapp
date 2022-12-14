describe('Splash page', () => {
  it('finds a logo and a signature in the Splash page', () => {
    cy.visit('http://web:3000')
    cy.url().should('include', '/')
    cy.get('[data-cy="logo"]')
    cy.get('[data-cy="signature"]')
  })

  it('redirects to the list of basins when clicking anywhere inside the Splash page', () => {
    cy.visit('http://web:3000')
    cy.get('[data-cy="logo"]').click()
    cy.url().should('include', '/basins')
  })

  it('jumps to the splash page when pressing the logo within the drawer menu', () => {
    cy.visit('http://web:3000/basins')
    cy.url().should('include', '/basins')
    cy.get('[data-cy="menu-icon"]').click()
    cy.get('[data-cy="drawer-logo"]').click()
    cy.get('[data-cy="logo"]')
  })
})

export {}
