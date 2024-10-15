import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import seaborn as sns
import numpy as np
import datetime
import os, sys, re
import cartopy.crs as ccrs
import cartopy.feature as cf
from extract_data import get_earthquakes
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER


class Marco():
    
    def __init__(
        self,
        latMin: float,
        latMax: float,
        longMin: float,
        longMax: float,
        startDate: str,
        endDate: str,
        intMin: float = -1,
        intMax: float = -1,
        magMin: float = -1,
        magMax: float = -1,
        profMin: float = -1,
        profMax: float = -1,
        cond: str = ''
    ):
      self.df = get_earthquakes(
            latMin,
            latMax,
            longMin,
            longMax,
            startDate,
            endDate,
            intMin,
            intMax,
            magMin,
            magMax,
            profMin,
            profMax,
            cond,
        )
      self.latMin = latMin
      self.latMax = latMax
      self.longMin = longMin
      self.longMax = longMax
      self.startDate = startDate
      self.endDate = endDate
    
    def save_to_csv(self):
      self.df.to_csv(
        f"./data/dataset_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}"
        )
    
    def save_to_excel(self):
      self.df.to_excel(
        excel_writer=f"./data/dataset_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}.xlsx",
        sheet_name="Hoja1"
      )

    

marco = Marco(
  latMin=26,
  latMax=45,
  longMin=-20,
  longMax=6,
  startDate="01/12/2023",
  endDate="12/10/2024",
  intMin=1,
  intMax=3,
  profMin=3,
  profMax=30
)

#marco.plot_map(fronteras=True, oceanos=True, rios=True)
#marco.plot_full_map_analysis()
marco.plot_int_time()
marco.save_to_excel()
