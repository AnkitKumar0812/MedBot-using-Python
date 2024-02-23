import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv("severity_of_disease.csv")
df = pd.DataFrame(data) 
disease= df['disease'].head(12)
severity = df['severity'].head(12)
# Horizontal Bar Plot
plt.scatter(disease[:10], severity[:10])
plt.scatter(disease,severity, color='r')
plt.xlabel("Diseases")
plt.ylabel("Severity")
plt.title("Severity of Disease")
plt.show()