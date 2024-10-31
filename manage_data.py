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
import pathlib
from scipy.optimize import curve_fit 
from scipy.special import factorial


class Marco():
    
    def __init__(
        self,
        path_to_file: str = '',
        latMin: float = 0,
        latMax: float = 0,
        longMin: float = 0,
        longMax: float = 0,
        startDate: str = '',
        endDate: str = '',
        intMin: float = -1,
        intMax: float = -1,
        magMin: float = -1,
        magMax: float = -1,
        profMin: float = -1,
        profMax: float = -1,
        cond: str = ''
    ):
      self.path = path_to_file

      if self.path == '':
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
        
      elif pathlib.Path(self.path).suffix == '.xlsx':
        self.df = pd.read_excel(io=self.path, sheet_name="Hoja1")

      elif pathlib.Path(self.path).suffix == '.csv':
        self.df = pd.read_csv(filepath_or_buffer=self.path)
      
      elif pathlib.Path(self.path).suffix == '.sqlite':
        pass

      else:
        self.df = pd.read_csv(filepath_or_buffer=self.path)

      self.latMin = latMin
      self.latMax = latMax
      self.longMin = longMin
      self.longMax = longMax
      self.startDate = startDate
      self.endDate = endDate
      self.profMin = profMin
      self.profMax = profMax
      self.magMin = magMin
      self.magMax = magMax
      self.cond = cond
      
    
    def save_to_csv(self):
      self.df.to_csv(
        f"./data/dataset_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}"
        )
    

    def save_to_excel(self):
      self.df.to_excel(
        excel_writer=f"./data/dataset_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}.xlsx",
        sheet_name="Hoja1"
      )

    def plot_map(
        self,
        fronteras=False,
        rios=False,
        oceanos=False,
        savefig=False,
        showfig=False
        ):

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

      if savefig == True:
        fig.savefig(f"./img/map_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()

    def plot_map_data(
        self,
        fronteras=False,
        rios=False,
        oceanos=False,
        savefig=False,
        showfig=False
        ):
       
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

      if savefig == True:
        fig.savefig(f"./img/map_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()
    

    def plot_full_map_analysis(
        self,
        savefig=False,
        showfig=False
        ):
      
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

      if savefig == True:
        fig.savefig(f"./img/full_analysis_map_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:  
        plt.show()
    

    def plot_int_time(
        self,
        savefig=False,
        showfig=False
        ):

      fig, ax = plt.subplots()
      self.df.plot.bar(x='Fecha', y='Int. max.', ax=ax)
      ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
      ax.set_xlabel("Fecha")
      ax.set_ylabel("Intensidad Máxima")
      fig.suptitle("Intensidad máxima de los terremotos registrados respecto del tiempo")
      ax.set_title(f"{self.df.Latitud.min()}/{self.df.Latitud.max()}ºN-{self.df.Longitud.min()}/{self.df.Longitud.max()}ºW")
      if savefig == True:
        fig.savefig(f"./img/int_timeseries_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()


    def plot_int_distribution(
        self,
        savefig=False,
        showfig=False,
        ):

      fig, ax = plt.subplots()
      self.df.plot.hist(by='Int. max.', bins=15, ax=ax)
      ax.set_xlabel("Intensidad Máxima")
      ax.set_xticks(np.arange(self.df.Intesidad.min(), self.df.Intensidad.max()+1, 0.5))
      fig.suptitle("Distribución de la intensidad máxima de los terremotos registrados respecto del tiempo")
      ax.set_title(f"{self.df.Latitud.min()}/{self.df.Latitud.max()}ºN-{self.df.Longitud.min()}/{self.df.Longitud.max()}ºW")
      if savefig == True:
        fig.savefig(f"./img/int_timeseries_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()


    def plot_mag_time(
        self,
        savefig=False,
        showfig=False
        ):

      fig, ax = plt.subplots()
      self.df.plot.bar(x='Fecha', y='Magnitud', ax=ax)
      ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
      ax.set_xlabel("Fecha")
      ax.set_ylabel("Magnitud Máxima")
      fig.suptitle("Magnitud máxima de los terremotos registrados respecto del tiempo")
      ax.set_title(f"{self.df.Latitud.min()}/{self.df.Latitud.max()}ºN-{self.df.Longitud.min()}/{self.df.Longitud.max()}ºW")
      if savefig == True:
        fig.savefig(f"./img/mag_timeseries_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()


    def plot_mag_distribution(
        self,
        savefig=False,
        showfig=False
        ):

      fig, ax = plt.subplots()
      self.df.Magnitud.plot.hist(bins=15, ax=ax)
      ax.set_xlabel("Magnitud")
      fig.suptitle("Distribución de la magnitud máxima de los terremotos registrados respecto del tiempo")
      ax.set_xticks(np.arange(self.df.Magnitud.min(), self.df.Magnitud.max()+1, 0.5))
      ax.set_title(f"{self.df.Latitud.min()}/{self.df.Latitud.max()}ºN-{self.df.Longitud.min()}/{self.df.Longitud.max()}ºW")
      if savefig == True:
        fig.savefig(f"./img/mag_timeseries_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()   

    def plot_mag_distribution_ritcher_law(
        self,
        savefig=False,
        showfig=False
    ): 
      fig = plt.figure()
      ax = self.df.Magnitud.plot.hist(bins=15)
      counts, bins = np.histogram(self.df.Magnitud, bins=15)
      ritcher = lambda x, a, b: 10**(a-b*x)
      popt, pcov = curve_fit(f=ritcher, xdata=bins[:-1], ydata=counts, p0=[1., 1.])
      pcov = np.sqrt(np.diag(pcov))
      ls = np.linspace(self.df.Magnitud.min(), self.df.Magnitud.max(), 500)
      ax.plot(ls, ritcher(ls, *popt), label="Ajuste Ritcher")
      ax.text(
        0.7, 0.5,
        '$N(M) = 10^{{ {}\\pm{}-{}\\pm{}*M }}$'.\
          format(np.round(popt[0], 3), np.round(pcov[0], 3), np.round(popt[1], 3), np.round(pcov[1], 3)),
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes
      )
      ax.legend()
      ax.set_xlabel("Magnitud")
      fig.suptitle("Distribución de la magnitud máxima de los terremotos registrados respecto del tiempo")
      ax.set_xticks(np.arange(self.df.Magnitud.min(), self.df.Magnitud.max()+1, 0.5))
      ax.set_title(f"{self.df.Latitud.min()}/{self.df.Latitud.max()}ºN-{self.df.Longitud.min()}/{self.df.Longitud.max()}ºW")
      if savefig == True:
        fig.savefig(f"./img/mag_timeseries_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()   
    

    def __poisson_analysis(
        self,
        savefig=False,
        showfig=False
        ):
    
      #### EN DESARROLLO
      poisson_dist = lambda k, t, A, c, p: (A*(c+t)**(-p))**k/factorial(k) * np.exp(A*(c+t)**(-p))
      print(poisson_dist(np.arange(1, 13, dtype=np.int32)))
      fig, ax = plt.subplots()
      ax.set_xlabel("Meses año")
      ax.hist(
        x=np.arange(1, 13),
        bins=poisson_dist(np.arange(1, 13, dtype=np.int32)),
        label="Número de terremotos esperados por mes",
        color='red',
        alpha=0.5
        ) 
      ax.hist(
        x=np.arange(1, 13),
        bins=poisson_dist(np.arange(1, 13, dtype=np.int32)),
        label="Número de terremotos esperados por mes (l+s)",
        color='blue',
        alpha=0.5
        )
      ax.hist(
        x=np.arange(1, 13),
        bins=poisson_dist(np.arange(1, 13, dtype=np.int32)),
        label="Número de terremotos esperados por mes (l-s)",
        color='green',
        alpha=0.5
        )
      if savefig == True:
        fig.savefig(f"./img/pois_dist_{str(datetime.datetime.now()).replace(":", "_").replace(".", "-").replace(" ", "__")}")
      if showfig == True:
        plt.show()        

marco = Marco(
  path_to_file=r"data\dataset_2024-10-16__21_17_22-633699"
#  latMin=26,
#  latMax=45,
#  longMin=-20,
#  longMax=6,
#  startDate="01/06/2023",
#  endDate="12/10/2024",
#  intMin=1,
#  intMax=8,
#  profMin=1,
#  profMax=100
)

#marco.plot_map(fronteras=True, oceanos=True, rios=True)
#marco.plot_full_map_analysis()
marco.save_to_csv()
marco.plot_mag_distribution_ritcher_law(showfig=True)
#marco.poisson_analysis(showfig=True)
#marco.save_to_excel()