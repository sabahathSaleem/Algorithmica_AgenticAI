from datetime import date
from pydantic import BaseModel, Field


class Payslip(BaseModel):
    """Represents the structured payroll, tax withholding, and employment details extracted from a payslip."""

    employee_id: str = Field(..., description="Unique identifier for the employee")
    employee_name: str = Field(..., description="Full name of the employee")
    pay_period_start: date = Field(..., description="Start date of the pay period")
    pay_period_end: date = Field(..., description="End date of the pay period")
    gross_income: float = Field(..., description="Total income before deductions")
    federal_tax: float = Field(..., description="Federal tax deduction amount")
    state_tax: float | None = Field(
        0.0, description="State tax deduction amount, if applicable"
    )
    social_security: float = Field(..., description="Social Security deduction amount")
    medicare: float = Field(..., description="Medicare deduction amount")
    other_deductions: float | None = Field(
        0.0, description="Other deductions (e.g., health insurance, retirement)"
    )
    net_income: float = Field(..., description="Income after all deductions")
    payment_date: date = Field(..., description="Date the payment was issued")
    hours_worked: float | None = Field(
        None, description="Total hours worked in the pay period"
    )
    hourly_rate: float | None = Field(
        None, description="Employee's hourly rate, if applicable"
    )