from pydantic import BaseModel, Field, field_validator


class Documento(BaseModel):
    id: int = Field(..., gt=0, description="ID único del documento, debe ser mayor que 0")
    nombre: str = Field(..., min_length=3, max_length=50, description="Nombre del documento")
    activo: bool
    tamano_mb: float = Field(..., gt=0, description="Tamaño del documento en MB, debe ser mayor que 0")
    categoria: str = Field(..., min_length=3, max_length=30, description="Categoría del documento")

    @field_validator("nombre")
    @classmethod
    def validar_nombre(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("El nombre no puede estar vacío")

        if value.isdigit():
            raise ValueError("El nombre no puede contener solo números")

        if len(value.split()) < 1:
            raise ValueError("El nombre debe tener contenido válido")

        return value

    @field_validator("categoria")
    @classmethod
    def validar_categoria(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("La categoría no puede estar vacía")

        if value.isdigit():
            raise ValueError("La categoría no puede contener solo números")

        return value