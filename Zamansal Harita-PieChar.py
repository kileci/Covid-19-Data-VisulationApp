import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# COVID-19 veri kaynağı
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'

# Veriyi yükleme
df = pd.read_csv(url)

# Veriyi dönüştürme: Sütunları tarih formatına dönüştürme
df['date'] = pd.to_datetime(df['date'])

# Veriyi hazırlama
fig_map = px.choropleth(df, 
                    locations="iso_code", 
                    color="total_cases", 
                    hover_name="location", 
                    animation_frame="date",
                    color_continuous_scale='viridis',
                    title="COVID-19 Günlük Vaka Sayısı Haritası",
                    labels={'total_cases': 'Vaka Sayısı'}
                   )
fig_map.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="LightGrey",
                showocean=True, oceancolor="LightBlue", showframe=False)
fig_map.update_layout(geo=dict(showframe=False, showcoastlines=False,
                           projection_type='equirectangular'),
                  margin=dict(l=0, r=0, t=40, b=0))

# Pasta grafiği oluşturma
top_countries = df.groupby('location')['total_cases'].max().nlargest(10)
fig_pie = go.Figure(data=[go.Pie(labels=top_countries.index, values=top_countries.values)])

fig_pie.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=12,
                  marker=dict(colors=px.colors.qualitative.Pastel, line=dict(color='#000000', width=2)))

fig_pie.update_layout(title="COVID-19 Toplam Vakaların Ülkelere Göre Dağılımı",
                  margin=dict(t=40, b=0, l=0, r=0))

# HTML dosyası olarak kaydetme
fig_map.show()
fig_pie.show()

fig_map.write_html("covid19_zaman_harita.html")
fig_pie.write_html("covid19_pie_chart.html")




