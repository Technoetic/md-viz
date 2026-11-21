# Usage: Rscript ggplot.R show.json output.svg
library(ggplot2)
args <- commandArgs(trailingOnly = TRUE)
queues <- jsonlite::fromJSON(args[1])$queues
samples <- stack(queues)
names(samples) <- c("time", "gate")
samples$gate <- factor(samples$gate, levels = names(queues))
palette <- c("#71E7E1", "#FE72B7", "#DAF777")
bg <- "#101425"
p <- ggplot(samples, aes(x = time, y = gate, fill = gate)) +
  geom_boxplot(width = 0.31, colour = "#CCD2E7", alpha = 0.5, outlier.shape = NA) +
  geom_point(position = position_jitter(height = 0.12, width = 0, seed = 17),
             shape = 21, size = 3.2, colour = "#101425", stroke = 0.6) +
  scale_fill_manual(values = palette, guide = "none") +
  scale_x_continuous(breaks = seq(0, 14, 2), limits = c(0, 14)) +
  labs(x = "Wait time (min)", y = NULL) +
  theme_minimal(base_size = 15) +
  theme(plot.background = element_rect(fill = bg, colour = NA),
        panel.background = element_rect(fill = bg, colour = NA),
        panel.grid.major.x = element_line(colour = "#32394E", linewidth = 0.4),
        panel.grid.major.y = element_blank(), panel.grid.minor = element_blank(),
        axis.text = element_text(colour = "#ECEFFC"), axis.title = element_text(colour = "#C8D0E2"),
        plot.margin = margin(10, 17, 8, 6))
svglite::svglite(args[2], width = 8.5, height = 2.95, bg = bg)
print(p)
invisible(dev.off())
