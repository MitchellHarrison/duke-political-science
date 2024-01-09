library(tidyverse)
library(shiny)
library(visNetwork)

RED <- "#f55f73"
BLUE <- "#5f76f5"

n_hubs <- 2
n_agents <- 20
total_nodes <- n_hubs + n_agents
p_consumes_diverse <- 0.3

nodes <- tibble(
  id = 1:total_nodes,
  shape = "icon",
  group = if_else(id %in% c(1,2), "hub", "agent"),
  icon.face = "FontAwesome",
  icon.color = rep(c(RED, BLUE), times = 5),
  icon.code = if_else(group == "hub", "f0c0", "f007"),
  icon.size = if_else(group == "hub", 75, 50)
)

edges <- tibble(
  from = c(rep(c(1,2), times = 4), 1),
  to = c(unlist(map2(c(3,5,7,9), c(4,6,8, 10), c)), 4),
  same_color = if_else(
    nodes[from, "icon.color"] == nodes[to, "icon.color"], 
    TRUE, 
    FALSE
  ),
  width = if_else(same_color, 10, 4)
)

server <- function(input, output) {
  output$mynetworkid <- renderVisNetwork({
    
    visNetwork(nodes, edges) |>
      visGroups(groupname = "hub", shape = "icon", 
                icon = list(code = "f0c0", size = 75)) |>
      visGroups(groupname = "agent", shape = "icon", 
                icon = list(code = "f007", size = 50)) |>
      addFontAwesome() 
  })
}

ui <- fluidPage(
  visNetworkOutput("mynetworkid")
)

shinyApp(ui = ui, server = server)