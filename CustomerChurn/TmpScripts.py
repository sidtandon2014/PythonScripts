data.groupby(["Number vmail messages"]).count().sort_values(by = "Id").to_csv("plot.csv")
sns.distplot(data["Customer service calls"],kde = False)

data.describe().to_csv("data_Describe.csv")
data[["State","Churn"]].groupby(["State"]).mean().sort_values("Churn")

sns.boxplot(x = 'Area code', y = 'Total eve minutes', hue = "Churn",data = data.sort_values("Churn"))



g = sns.FacetGrid(data, col="State", col_wrap = 10)
g = g.map(sns.boxplot, "Churn","Total day minutes")


len(np.unique(data["State"]))
