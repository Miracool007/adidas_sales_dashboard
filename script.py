# Importing the needed libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Defining the layout of my streamlit page
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Streamlit Dashboard Title
st.title("Adidas Sales Dashboard 📊")

# Loading my Dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    return df

df = load_data()

# Creating my Slicers
retailer_options = ["All"] + sorted(df["Retailer"].unique().tolist())
month_options = ["All"] + sorted(df["Month"].unique().tolist())
state_options = ["All"] + sorted(df["State"].unique().tolist())
revenue = df["Total Sales"].sum()

# Adding the slicers to my sidebar menu
st.sidebar.header("🔍 Slicers")
with st.sidebar.form(key="filter_form"):
    retailer = st.selectbox("Retailer", retailer_options)
    month = st.selectbox("Month", month_options)
    state = st.selectbox("States", state_options)

    apply_filter = st.form_submit_button("Apply Filters")

# Specifying the action to be performed if the "Apply Filter" button is pressed
if apply_filter:
    filter_df = df.copy()

    if retailer != "All":
        filter_df = filter_df[filter_df["Retailer"] == retailer]
    if month != "All":
        filter_df = filter_df[filter_df["Month"] == month]
    if state != "All":
        filter_df = filter_df[filter_df["State"] == state]

    revenue = filter_df["Total Sales"].sum()

else:
    filter_df = df.copy()


#Creating my Key Metrics
col1, col2, col3, col4 = st.columns(4)

col1.metric("📅 Total Months in Review", df["Month"].nunique())
col2.metric("🛒 Number of Retailers", df["Retailer"].nunique())
col3.metric("🏙️ Total States in Review", df["State"].nunique())
col4.metric("💸 Total Revenue Generated", df["Total Sales"].sum())

# Creating the metrics for the selected values from the slicers
st.markdown("### Selected Values")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Selected Month", month)
col6.metric("Selected Retailer", retailer)
col7.metric("Selected State", state)
col8.metric("Total Revenue of selected metrics", revenue)

#Creating the first two charts
chart1, chart2 = st.columns((5,5))

with chart1:
    st.markdown("### 🏪 Total Sales per Retailer")
    fig, ax = plt.subplots()
    chart = sns.countplot(data=filter_df, x="Retailer", hue="Retailer", ax=ax)
    plt.xticks(rotation=45)
    plt.xlabel("Retailers")
    plt.ylabel("Total Sales")
    
    # Adding Data Labels to the chart
    for bar in chart.patches:
        count = bar.get_height()
        if count > 0:  # Only show label for visible bars
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                count + 0.5,                     
                f'{int(count)}',                
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight='bold',
                color='black'
            )
    st.pyplot(fig)

with chart2:
    st.markdown("### 📅 Revenue Distribution per Month")
    fig, ax = plt.subplots()
    sns.lineplot(data=filter_df, x="Month", y="Total Sales", ax=ax)

    plt.xticks(rotation=45)  
    st.pyplot(fig)

# Creating the next two charts
ch1, ch2 = st.columns((5,5))

with ch1:
    st.markdown("### 🗺️ Total Sales per Region")
    counts = df["Region"].value_counts()
    labels = counts.index
    values = counts.values

    # Adding Data Labels to the Pie-Chart
    def format_label(pct, all_vals):
        absolute = int(round(pct/100 * sum(all_vals)))
        return f"{pct:.1f}%\n({absolute})"

    fig, ax = plt.subplots()
    plt.pie(
        values,
        labels=labels,
        autopct=lambda pct: format_label(pct, values)
    )
    st.pyplot(fig)

with ch2:
    st.markdown("### 📦 Revenue Generated per Product")
    fig, ax = plt.subplots()
    ch = ax.bar(x=df["Product"], height=df["Total Sales"])

    plt.xticks(rotation=45)
    st.pyplot(fig)

# The dataset I'm working with contains states in the USA. The best option to visualize the revenue_per_state is using the map Chart.
# To use this map chart on the plotly.graph_objects library, there are certain conditions you need to apply.
# Firstly you have to get the abbreviations of all the states, and store it as a dictionary, example below;

state_abbrev = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR',
    'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT',
    'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI',
    'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA',
    'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME',
    'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI',
    'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
    'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH',
    'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
    'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV',
    'Wisconsin': 'WI', 'Wyoming': 'WY'
}

# Map each state on the "State" column in your dataset to their abbrevations
filter_df["abbrev"] = filter_df["State"].map(state_abbrev)

# Next thing is to get the cordinates of all the states and store it in a dictionary format, example below. 
# You can simply get this using ChatGPT

state_coords = {
    'New York': [43.0000, -75.0000],
    'Texas': [31.0000, -100.0000],
    'California': [36.7783, -119.4179],
    'Illinois': [40.0000, -89.0000],
    'Pennsylvania': [41.2033, -77.1945],
    'Nevada': [39.5000, -117.0000],
    'Colorado': [39.1130, -105.3589],
    'Washington': [47.7511, -120.7401],
    'Florida': [27.9944, -81.7603],
    'Minnesota': [46.7296, -94.6859],
    'Montana': [46.8797, -110.3626],
    'Tennessee': [35.5175, -86.5804],
    'Nebraska': [41.4925, -99.9018],
    'Alabama': [32.3182, -86.9023],
    'Maine': [45.2538, -69.4455],
    'Alaska': [64.2008, -149.4937],
    'Hawaii': [20.7967, -156.3319],
    'Wyoming': [43.0759, -107.2903],
    'Virginia': [37.4316, -78.6569],
    'Michigan': [44.1822, -84.5068],
    'Missouri': [38.5739, -92.6038],
    'Utah': [39.3200, -111.0937],
    'Oregon': [43.8041, -120.5542],
    'Louisiana': [30.9843, -91.9623],
    'Idaho': [44.0682, -114.7420],
    'Arizona': [34.0489, -111.0937],
    'New Mexico': [34.5199, -105.8701],
    'Georgia': [32.1656, -82.9001],
    'South Carolina': [33.8361, -81.1637],
    'North Carolina': [35.7596, -79.0193],
    'Ohio': [40.4173, -82.9071],
    'Kentucky': [37.8393, -84.2700],
    'Mississippi': [32.3547, -89.3985],
    'Arkansas': [35.2010, -91.8318],
    'Oklahoma': [35.4676, -97.5164],
    'Kansas': [39.0119, -98.4842],
    'South Dakota': [43.9695, -99.9018],
    'North Dakota': [47.5515, -101.0020],
    'Iowa': [41.8780, -93.0977],
    'Wisconsin': [44.5000, -89.5000],
    'Indiana': [40.2672, -86.1349],
    'West Virginia': [38.5976, -80.4549],
    'Maryland': [39.0458, -76.6413],
    'Delaware': [38.9108, -75.5277],
    'New Jersey': [40.0583, -74.4057],
    'Connecticut': [41.6032, -73.0877],
    'Rhode Island': [41.5801, -71.4774],
    'Massachusetts': [42.4072, -71.3824],
    'Vermont': [44.5588, -72.5778],
    'New Hampshire': [43.1939, -71.5724],
}

# Then create two new columns "lat" (short for latitude) and "lon" (short for longitude). Mapping each state's longitude and latitude 
filter_df['lat'] = filter_df['State'].map(lambda x: state_coords.get(x, [None, None])[0])
filter_df['lon'] = filter_df['State'].map(lambda x: state_coords.get(x, [None, None])[1])

state_sales = filter_df.groupby("abbrev")["Total Sales"].sum().reset_index()
tet = state_sales["abbrev"] + ": $" + state_sales["Total Sales"].apply(lambda x: f"{x:,.0f}")

# Creating the map chart
fig = go.Figure()
fig.add_trace(go.Choropleth(
    locations=state_sales['abbrev'],
    z=state_sales['Total Sales'],
    locationmode='USA-states',
    colorscale='plasma',
    colorbar_title="Total Sales",
    geo='geo'
))

# Add state labels on top

fig.add_trace(go.Scattergeo(
    locationmode='USA-states',
    lon=filter_df['lon'],
    lat=filter_df['lat'],
    text=tet,
    mode='markers',
    marker=dict(size=5, color='black'),  # Customize as needed
    hoverinfo="text",
    showlegend=False
))

# Map layout
fig.update_layout(
    geo_scope='usa'
)

# Show in Streamlit
st.markdown("### 🌍 Distribution of Revenue across States")
st.plotly_chart(fig)

# Adding a preview of the dataset used
st.markdown("### 🧾 Data Preview")
st.dataframe(data=df.head(20))

# Adding my Socials 😏
st.markdown('''
----
### Created with ❤️ by Miracle 😊\n
<a href="https://www.linkedin.com/in/miracle-aniobi-6380292a0?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3B8zG0riqUTV%2BAWaa33S%2F2pQ%3D%3D" target="_blank"> 🌐 LinkedIn </a><br>
<a href="https://github.com/Miracool007" target="_blank"> 📊 GitHub </a><br>

''', unsafe_allow_html=True)

# After going through and copying this, I hope you all can be able to create your own interactive visuals using the streamlit library🙏
