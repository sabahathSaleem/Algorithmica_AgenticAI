from pydantic import BaseModel, Field

class Address(BaseModel):
    """Represents the geographic location details of a person or organization."""

    street: str | None = Field(
        None, description="The street address, e.g., 123 Main St"
    )
    city: str | None = Field(None, description="The city, e.g., Springfield")
    state: str | None = Field(None, description="The state or province code, e.g., IL")
    postal_code: str | None = Field(
        None, description="The postal or ZIP code, e.g., 62704"
    )
    country: str | None = Field(None, description="The country, e.g., USA")


class LineItem(BaseModel):
    """Represents an individual product or service entry listed in a document."""

    amount: float = Field(..., description="The total amount for this line item")
    description: str | None = Field(
        None, description="Description of the product/service, e.g., Laptop"
    )
    product_code: str | None = Field(
        None, description="The SKU or product code, e.g., LPT-001"
    )
    quantity: int = Field(..., description="The number of units")
    unit: str | None = Field(None, description="Unit of measure, e.g., pcs")
    unit_price: float = Field(..., description="Price per single unit")


class VAT(BaseModel):
    """Represents Value Added Tax details, including rates and calculated amounts."""

    amount: float = Field(..., description="Taxable amount")
    category_code: str | None = Field(None, description="Tax category code, e.g., A")
    tax_amount: float | None = Field(None, description="The calculated tax value")
    tax_rate: float | None = Field(
        None, description="Percentage as a float, e.g., 10 for 10%"
    )
    total_amount: float = Field(..., description="Total amount including tax")


class Party(BaseModel):
    """Represents the contact and identification details of a transacting entity."""

    name: str = Field(..., description="Name of the entity, e.g., Google")
    street: str | None = Field(None, description="Street address")
    city: str | None = Field(None, description="City name")
    state: str | None = Field(None, description="State or province")
    postal_code: str | None = Field(None, description="Postal code")
    country: str | None = Field(None, description="Country name")
    email: str | None = Field(None, description="Contact email address")
    phone: str | None = Field(None, description="Contact phone number")
    website: str | None = Field(None, description="Entity website URL")
    tax_id: str | None = Field(None, description="Tax identification number")
    registration: str | None = Field(None, description="Business registration number")
    iban: str | None = Field(None, description="International Bank Account Number")
    payment_ref: str | None = Field(
        None, description="Payment reference or invoice number"
    )


class Invoice(BaseModel):
    """Represents the comprehensive structured data extracted from an invoice document."""

    invoice_id: str = Field(..., description="The unique identifier of the invoice")
    invoice_date: str = Field(
        ..., description="The date the invoice was issued (YYYY-MM-DD)"
    )
    supplier: Party
    receiver: Party
    line_items: list[LineItem]
    vat: list[VAT]