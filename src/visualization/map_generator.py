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

    def generate_multirat_map(
        self,
        lte_cell_table,
        cell_5g_table,
        coverage_grid,
        output_file="outputs/multirat_coverage_map.html"
    ):

        center_lat = lte_cell_table["latitude"].median()
        center_lon = lte_cell_table["longitude"].median()

        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12
        )

        # ------------------------------------------------
        # LAYER 1: LTE CELLS
        # ------------------------------------------------

        lte_layer = folium.FeatureGroup(
            name="LTE Cells"
        )

        for _, row in lte_cell_table.iterrows():

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
            <b>LTE Cell ID:</b> {row['cell_id']}<br>
            <b>Site ID:</b> {row['enb_id']}<br>
            <b>PCI:</b> {row['pci']}<br>
            <b>Health:</b> {row['health_score']:.2f}<br>
            <b>Issue:</b> {row['issue']}
            """

            folium.CircleMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                radius=6,
                popup=popup_text,
                color=color,
                fill=True,
                fill_opacity=0.8
            ).add_to(
                lte_layer
            )

        lte_layer.add_to(m)

        # ------------------------------------------------
        # LAYER 2: 5G CELLS (KNOWN SITE POSITIONS ONLY)
        # ------------------------------------------------

        nr_layer = folium.FeatureGroup(
            name="5G Cells"
        )

        for _, row in cell_5g_table.iterrows():

            popup_text = f"""
            <b>5G gNB:</b> {row['gnb_id_dummy']}<br>
            <b>5G Cell:</b> {row['cell_id_dummy']}<br>
            <b>PCI:</b> {row['pci']}<br>
            <b>Height:</b> {row['height_m']} m<br>
            <b>Azimuth:</b> {row['azimuth_deg']}&deg;
            """

            folium.RegularPolygonMarker(
                location=[
                    row["latitude"],
                    row["longitude"]
                ],
                number_of_sides=3,
                radius=8,
                popup=popup_text,
                color="black",
                fill_color="cyan",
                fill_opacity=0.9
            ).add_to(
                nr_layer
            )

        nr_layer.add_to(m)

        # ------------------------------------------------
        # LAYER 3: BEST AVAILABLE SIGNAL (GRID)
        # ------------------------------------------------

        best_layer = folium.FeatureGroup(
            name="Best Signal (LTE vs 5G)",
            show=False
        )

        for _, row in coverage_grid.iterrows():

            color = "cyan" if row["winner"] == "5G" else "orange"

            popup_text = f"""
            <b>Winner:</b> {row['winner']}<br>
            <b>LTE score:</b> {row['lte_score']}<br>
            <b>5G score:</b> {row['nr_score']}<br>
            <b>LTE samples:</b> {row['lte_samples']}<br>
            <b>5G samples:</b> {row['nr_samples']}
            """

            folium.CircleMarker(
                location=[
                    row["grid_lat"],
                    row["grid_lon"]
                ],
                radius=4,
                popup=popup_text,
                color=color,
                fill=True,
                fill_opacity=0.6,
                weight=0
            ).add_to(
                best_layer
            )

        best_layer.add_to(m)

        folium.LayerControl(
            collapsed=False
        ).add_to(m)

        legend_html = """
        <div style="
        position: fixed;
        bottom: 50px;
        left: 50px;
        width: 210px;
        background-color: white;
        border:2px solid grey;
        z-index:9999;
        font-size:14px;
        padding: 10px;
        ">

        <b>LTE Cell Issue</b><br>
        <span style="color:red;">●</span> Coverage<br>
        <span style="color:blue;">●</span> Quality<br>
        <span style="color:purple;">●</span> Performance<br>
        <span style="color:green;">●</span> Healthy<br>
        <br>
        <b>5G Site</b><br>
        <span style="color:cyan;">&#9650;</span> Known 5G Cell<br>
        <br>
        <b>Best Signal (Grid)</b><br>
        <span style="color:orange;">●</span> LTE wins<br>
        <span style="color:cyan;">●</span> 5G wins

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
            f"\nMulti-RAT map saved to: {output_file}"
        )