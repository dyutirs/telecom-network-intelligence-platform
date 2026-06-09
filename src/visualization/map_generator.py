import folium


class MapGenerator:

    def generate_bad_cell_map(
        self,
        cell_table,
        output_file="outputs/bad_cells_map.html"
    ):

        center_lat = cell_table["latitude"].median()
        center_lon = cell_table["longitude"].median()

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12
        )

        all_cells_layer = folium.FeatureGroup(
            name="All Cells"
        )

        bad_cells_layer = folium.FeatureGroup(
            name="Bad Cells Only"
        )

        for _, row in cell_table.iterrows():

            issue = row["issue"]

            if issue == "Coverage":
                color = "red"

            elif issue == "Quality":
                color = "blue"

            elif issue == "Performance":
                color = "purple"

            else:
                color = "green"

            popup_text = f"""
            <b>Cell ID:</b> {row['cell_id']}<br>
            <b>Site ID:</b> {row['enb_id']}<br>
            <b>PCI:</b> {row['pci']}<br>
            <b>Health:</b> {row['health_score']:.2f}<br>
            <b>Issue:</b> {row['issue']}<br>
            <b>Confidence:</b> {row['confidence']}%
            """

            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=7,
                popup=popup_text,
                color=color,
                fill=True,
                fill_opacity=0.8
            ).add_to(
                all_cells_layer
            )

            if row["issue"] != "Healthy":

                folium.CircleMarker(
                    location=[
                        row["latitude"],
                        row["longitude"]
                    ],
                    radius=7,
                    popup=popup_text,
                    color=color,
                    fill=True,
                    fill_opacity=0.8
                ).add_to(
                    bad_cells_layer
                )

        all_cells_layer.add_to(m)

        bad_cells_layer.add_to(m)

        folium.LayerControl(
            collapsed=False
        ).add_to(m)

        legend_html = """
        <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 180px;
        height: 140px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        ">

        <b>RCA Legend</b><br>

        <span style="color:red;">●</span> Coverage<br>
        <span style="color:blue;">●</span> Quality<br>
        <span style="color:purple;">●</span> Performance<br>
        <span style="color:green;">●</span> Healthy

        </div>
        """

        m.get_root().html.add_child(
            folium.Element(
                legend_html
            )
        )

        m.save(
            output_file
        )

        print(
            f"\nMap saved to: {output_file}"
        )