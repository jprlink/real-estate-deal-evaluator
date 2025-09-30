"""
CLI interface using Typer.

Usage:
    python -m backend.cli.main evaluate --help
    python -m backend.cli.main research --address "10 Rue de Rivoli, 75001 Paris"
"""

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

app = typer.Typer(help="Real Estate Deal Evaluator CLI")
console = Console()


@app.command()
def evaluate(
    address: str = typer.Option(..., "--address", "-a", help="Property address"),
    price: float = typer.Option(..., "--price", "-p", help="Property price (EUR)"),
    surface: float = typer.Option(..., "--surface", "-s", help="Surface area (m²)"),
    rooms: int = typer.Option(..., "--rooms", "-r", help="Number of rooms"),
    down_payment: float = typer.Option(..., "--down-payment", help="Down payment (EUR)"),
    loan_amount: float = typer.Option(..., "--loan-amount", help="Loan amount (EUR)"),
    annual_rate: float = typer.Option(0.03, "--annual-rate", help="Annual interest rate"),
    loan_term: int = typer.Option(20, "--loan-term", help="Loan term (years)"),
    monthly_rent: float = typer.Option(2000, "--monthly-rent", help="Expected monthly rent (EUR)"),
):
    """
    Evaluate a property investment opportunity.

    Example:
        python -m backend.cli.main evaluate \\
            --address "10 Rue de Rivoli, 75001 Paris" \\
            --price 500000 \\
            --surface 50 \\
            --rooms 2 \\
            --down-payment 100000 \\
            --loan-amount 400000
    """
    console.print(Panel.fit(
        "[bold blue]Real Estate Deal Evaluator[/bold blue]\\n" +
        f"Analyzing: {address}",
        border_style="blue"
    ))

    # Import calculation modules
    from backend.calculations import financial, mortgage

    # Calculate metrics
    monthly_payment = mortgage.monthly_payment(loan_amount, annual_rate, loan_term)
    gmi = financial.gross_monthly_income(monthly_rent)
    vcl = financial.vacancy_credit_loss(gmi, 0.05)
    noi = financial.noi_calculation(gmi, vcl, 6000)  # Placeholder annual OE
    ads = financial.annual_debt_service(monthly_payment)
    dscr = financial.dscr_calculation(noi, ads)
    cap_rate = financial.cap_rate(noi, price)

    # Create results table
    table = Table(title="Financial Analysis", show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Property Price", f"€{price:,.0f}")
    table.add_row("Price per m²", f"€{price/surface:,.0f}")
    table.add_row("Monthly Payment", f"€{monthly_payment:,.2f}")
    table.add_row("NOI (Annual)", f"€{noi:,.2f}")
    table.add_row("DSCR", f"{dscr:.2f}")
    table.add_row("Cap Rate", f"{cap_rate*100:.2f}%")

    console.print(table)

    # Verdict
    if dscr > 1.2:
        verdict = "[bold green]BUY[/bold green] - Positive cash flow"
    elif dscr > 1.0:
        verdict = "[bold yellow]CAUTION[/bold yellow] - Marginal cash flow"
    else:
        verdict = "[bold red]PASS[/bold red] - Negative cash flow"

    console.print(f"\\nVerdict: {verdict}")


@app.command()
def research(
    address: str = typer.Option(..., "--address", "-a", help="Property address to research")
):
    """
    Research property market data (DVF comps, rent caps, risks).

    Example:
        python -m backend.cli.main research --address "10 Rue de Rivoli, 75001 Paris"
    """
    console.print(f"[cyan]Researching property at: {address}[/cyan]")
    console.print("[yellow]Note: Full research agent integration pending API keys[/yellow]")


@app.command()
def negotiate(
    address: str = typer.Option(..., "--address", "-a", help="Property address"),
    asking_price: float = typer.Option(..., "--asking", help="Asking price (EUR)"),
    offer_price: float = typer.Option(..., "--offer", help="Your offer price (EUR)"),
    draft: bool = typer.Option(False, "--draft", help="Create Gmail draft"),
):
    """
    Generate negotiation email draft.

    Example:
        python -m backend.cli.main negotiate \\
            --address "10 Rue de Rivoli, 75001 Paris" \\
            --asking 500000 \\
            --offer 465000 \\
            --draft
    """
    discount = ((asking_price - offer_price) / asking_price) * 100
    console.print(f"[cyan]Negotiation Analysis[/cyan]")
    console.print(f"Property: {address}")
    console.print(f"Asking: €{asking_price:,.0f}")
    console.print(f"Offer: €{offer_price:,.0f}")
    console.print(f"Discount: {discount:.1f}%")

    if draft:
        console.print("[yellow]Note: Gmail draft creation requires OAuth setup[/yellow]")


if __name__ == "__main__":
    app()