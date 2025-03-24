from sqlalchemy import ForeignKey, Integer, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from datetime import datetime
from environment_app.flask_app import db


class Borough(db.Model):
    __tablename__ = 'Borough'
    
    borough_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    borough_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relationships
    energy_consumptions: Mapped[List["EnergyConsumption"]] = relationship(back_populates="borough")
    ghg_emissions: Mapped[List["GHGEmission"]] = relationship(back_populates="borough")


class Sector(db.Model):
    __tablename__ = 'Sector'
    
    sector_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sector_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relationships
    energy_consumptions: Mapped[List["EnergyConsumption"]] = relationship(back_populates="sector")
    ghg_emissions: Mapped[List["GHGEmission"]] = relationship(back_populates="sector")


class Type(db.Model):
    __tablename__ = 'Type'
    
    type_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type_name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Relationships
    energy_consumptions: Mapped[List["EnergyConsumption"]] = relationship(back_populates="type")
    ghg_emissions: Mapped[List["GHGEmission"]] = relationship(back_populates="type")


class EnergyConsumption(db.Model):
    __tablename__ = 'Energy_Consumption'
    
    consumption_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    borough_id: Mapped[int] = mapped_column(Integer, ForeignKey('Borough.borough_id'))
    sector_id: Mapped[int] = mapped_column(Integer, ForeignKey('Sector.sector_id'))
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('Type.type_id'))
    year: Mapped[int] = mapped_column(Integer)
    consumption: Mapped[float] = mapped_column(Float)
    
    # Relationships
    borough: Mapped["Borough"] = relationship(back_populates="energy_consumptions")
    sector: Mapped["Sector"] = relationship(back_populates="energy_consumptions")
    type: Mapped["Type"] = relationship(back_populates="energy_consumptions")


class GHGEmission(db.Model):
    __tablename__ = 'GHG_Emission'
    
    emission_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    borough_id: Mapped[int] = mapped_column(Integer, ForeignKey('Borough.borough_id'))
    sector_id: Mapped[int] = mapped_column(Integer, ForeignKey('Sector.sector_id'))
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey('Type.type_id'))
    year: Mapped[int] = mapped_column(Integer)
    emission: Mapped[float] = mapped_column(Float)
    
    # Relationships
    borough: Mapped["Borough"] = relationship(back_populates="ghg_emissions")
    sector: Mapped["Sector"] = relationship(back_populates="ghg_emissions")
    type: Mapped["Type"] = relationship(back_populates="ghg_emissions")

class Feedback(db.Model):
    __tablename__ = 'feedback'  # Note: using lowercase table name to follow SQLite conventions
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    submitted_at: Mapped[str] = mapped_column(String(50), nullable=False)