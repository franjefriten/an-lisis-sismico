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

    def plot_map(self, fronteras=False, rios=False, oceanos=False):
       
      norma_color = Normalize(vmin=self.df.Magnitud.min(), vmax=self.df.Magnitud.max())
      norma_tamanno = Normalize(vmin=self.df.Profundidad.min(), vmax=self.df.Profundidad.max())

      print("Magnitud max", self.df.Magnitud.max(), "Tipo", self.df.Magnitud.dtype)
      print("Magnitud min", self.df.Magnitud.min())
      print("Profundidad max", self.df.Profundidad.max(), "Tipo", self.df.Profundidad.dtype)
      print("Profundidad min", self.df.Profundidad.min())
      
      fig = plt.figure(figsize=(10, 10))
      ax = plt.axes(projection=ccrs.PlateCarree())
      ax.add_feature(cf.COASTLINE)
      ax.add_feature(cf.LAND)
      if fronteras == True:
        ax.add_feature(cf.BORDERS)
      if rios == True:
        ax.add_feature(cf.RIVERS)
      if oceanos == True:
        ax.add_feature(cf.OCEAN)
      ax.set_extent([self.df.Longitud.min(), self.df.Longitud.max(), self.df.Latitud.min(), self.df.Latitud.max()])
      ax.set_title('Terremotos en {}/{} ºN y {}/{} ºS'.format(self.df.Longitud.min(), self.df.Longitud.max(), self.df.Latitud.min(), self.df.Latitud.max()))
      ax.set_xlabel('Longitud')
      ax.set_ylabel('Latitud')

      sns.scatterplot(x='Longitud', y='Latitud', data=self.df, hue='Magnitud', palette='hot_r', alpha=0.6, transform=ccrs.PlateCarree(),
                      size='Profundidad', hue_norm=norma_color, size_norm=norma_tamanno, sizes=(1, 50), ax=ax)
      
      ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)
     
      plt.show()

marco = Marco(
  latMin=26,
  latMax=45,
  longMin=-20,
  longMax=6,
  startDate="01/01/2024",
  endDate="12/10/2024",
  intMin=1,
  intMax=3,
  profMin=3,
  profMax=30
)

marco.plot_map(fronteras=True, oceanos=True, rios=True)