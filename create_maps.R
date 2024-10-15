library(plotly)
library(dplyr)

plot_map <- function(path_to_csv, path_to_store, width, height) {

  df <- read.csv(path_to_csv)
  str(df)
  g <- list(
    scope = "spain",
    projection = list(type = "mercator"),
    showland = TRUE,
    landcolor = toRGB("gray95"),
    subunitcolor = toRGB("gray85"),
    countrycolor = toRGB("gray85"),
    countrywidth = 0.5,
    subunitwidth = 0.5,
    lonaxis = list(range = c(min(df$Longitud) - 5, max(df$Longitud) + 5)),
    lataxis = list(range = c(min(df$Latitud) - 5, max(df$Latitud) + 5))
  )
  yaxis <- list(
    automargin = TRUE
  )

  fig <- plot_geo(
    df,
    lat = ~Latitud,
    lon = ~Longitud,
    width = width,
    height = height
  )

  fig <- fig %>% add_markers(
    text = ~paste(
      paste("Magnitud: ", Magnitud),
      paste("Profundidad: ", Profundidad),
      sep = "<br />"
    ),
    color = ~Magnitud,
    symbol = I("circle"),
    size = ~Profundidad,
    hoverinfo = "text"
  )
  fig <- fig %>% colorbar(title = "Magnitud de terremotos<br />")
  fig <- fig %>% layout(
    title = "Mapa de terremotos",
    geo = g,
    autosize = FALSE,
    yaxis = yaxis
  )

  path <- path_to_store
  path <- paste(
    path,
    gsub("/", "-", gsub(":", "_", gsub(" ", "__", Sys.time()))),
    ".html",
    sep = ""
  )
  cat(path)
  htmltools::save_html(
    as_widget(fig),
    path
    )
}


#plot_map(
#  "C:\\Users\\kikof\\Desktop\\Máster\\PR, Visualizacion de datos-20241012T164733Z-001\\PR, Visualizacion de datos\\Proyecto\\data\\dataset_2024-10-13__17_51_34-916597",
#  "C:\\Users\\kikof\\Desktop\\Máster\\PR, Visualizacion de datos-20241012T164733Z-001\\PR, Visualizacion de datos\\Proyecto\\img\\",
#  width = 800,
#  height = 800
#  )

