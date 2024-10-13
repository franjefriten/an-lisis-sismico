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

    def plot_map(self, fronteras=False, rios=False, oceanos=False):
       
      norma_color = Normalize(vmin=self.df.Magnitud.min(), vmax=self.df.Magnitud.max())
      norma_tamanno = Normalize(vmin=self.df.Profundidad.min(), vmax=self.df.Profundidad.max())
      
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
      ax.set_extent([self.df.Longitud.min()-5, self.df.Longitud.max()+5, self.df.Latitud.min()-5, self.df.Latitud.max()+5])
      ax.set_title('Terremotos en {}/{} ºN y {}/{} ºE'.format(self.df.Longitud.min(), self.df.Longitud.max(), self.df.Latitud.min(), self.df.Latitud.max()))
      ax.set_xlabel('Longitud')
      ax.set_ylabel('Latitud')

      sns.scatterplot(x='Longitud', y='Latitud', data=self.df, hue='Magnitud', palette='hot_r', alpha=0.6, transform=ccrs.PlateCarree(),
                      size='Profundidad', hue_norm=norma_color, size_norm=norma_tamanno, sizes=(1, 50), ax=ax)
      
      ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True)

      fig.savefig(f"./img/map_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      plt.show()
    
    def plot_full_map_analysis(self):
      
      # Preambumos
      max_mag = self.df.Magnitud.max()
      min_mag = self.df.Magnitud.min()
      norma_color = Normalize(vmin=self.df.Magnitud.min(), vmax=self.df.Magnitud.max())
      norma_tamanno = Normalize(vmin=self.df.Profundidad.min(), vmax=self.df.Profundidad.max())

      font = {'family': 'serif',
              'color':  'black',
              }

      n = 12 # Editar si se ve necesario
      delta_mag = (max_mag - min_mag) / n

      fig = plt.figure(figsize=(10, 8), dpi=120)
      fig.suptitle("Análisis sísmico {}/{} ºN y {}/{} ºE".format(self.df.Longitud.min(), self.df.Longitud.max(), self.df.Latitud.min(), self.df.Latitud.max()),
                   fontdict=font,
                   fontsize=14)
      gs = fig.add_gridspec(3,3)
      ax_map = fig.add_subplot(gs[:2, :2], projection=ccrs.PlateCarree())
      ax_depth = fig.add_subplot(gs[2, :2])
      ax_mag = fig.add_subplot(gs[:2, 2])
      ax_scat = fig.add_subplot(gs[2, 2])

      ax_map.add_feature(cf.COASTLINE)
      ax_map.add_feature(cf.LAND)
      ax_map.set_extent([self.df.Longitud.min(), self.df.Longitud.max(), self.df.Latitud.min(), self.df.Latitud.max()])

      gl = ax_map.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                        linewidth=2, color='gray', alpha=0.5, linestyle='--')
      gl.xlabels_top = False
      gl.ylabels_left = False
      gl.xformatter = LONGITUDE_FORMATTER
      gl.yformatter = LATITUDE_FORMATTER
      gl.xlabel_style = {'size': 15, 'color': 'gray'}
      gl.xlabel_style = {'color': 'red', 'weight': 'bold'}

      sns.scatterplot(x='Longitud', y='Latitud', data=self.df, hue='Magnitud', palette='hot_r',
                      alpha=0.8, transform=ccrs.PlateCarree(),
                      size='Profundidad', hue_norm=norma_color, size_norm=norma_tamanno, sizes=(1, 50), ax=ax_map, legend="brief")

      sns.histplot(y='Magnitud',
                   data=self.df,
                   bins=n,
                   binrange=[min_mag, max_mag],
                   ax=ax_mag,
                   stat="frequency")

      sns.boxplot(data=self.df,
                  x='Year',
                  y='Profundidad',
                  showfliers=False,
                  ax=ax_depth)

      sns.regplot(data=self.df,
                  x='Magnitud',
                  y='Profundidad',
                  ax=ax_scat,
                  robust=True,
                  marker='x',
                  line_kws=dict(color="r"))

      fig.tight_layout(rect=(0, 0, 1, 0.98))
      fig.savefig(f"./img/full_analysis_map_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      plt.show()

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

marco.plot_map(fronteras=True, oceanos=True, rios=True)
marco.plot_full_map_analysis()