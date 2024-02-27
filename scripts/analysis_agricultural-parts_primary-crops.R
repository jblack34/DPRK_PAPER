library(readr)
library(dplyr)

data1 <- read_csv("FAOSTAT_primery_crops.csv") 
data3 <- read_csv("OECD_Parts_Agricultural.csv") 
data1 <- data1 %>%
  group_by(Year) %>%
  summarise(Total_Value = sum(`Value`, na.rm = TRUE))

data3 <- data3 %>%
  group_by(Year) %>%
  summarise(Total_Trade_Value = sum(`Trade Value`, na.rm = TRUE))

merged_data2 <- merge(data1, data3, by = "Year")

model2 <- lm(Total_Value ~ Total_Trade_Value, data = merged_data2)

summary(model2)

plot(merged_data2$Total_Trade_Value, merged_data2$Total_Value, 
     xlab = "Import of Agricultural spare parts in US $", ylab = "Production of primary crops in t", 
     main = "Scatterplot with Regression Line")
abline(model2, col = "red")