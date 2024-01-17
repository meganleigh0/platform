    # Add annotations for each bar
        for index, row in department_utilization.iterrows():
            fig.add_annotation(
                x=row['Department'],
                y=row['Utilization'],
                text=f"{row['Utilization']:.1f}%",  # Format the utilization value and append a percent sign
                showarrow=False,
                row=2,
                col=i,
                yshift=10  # Adjust this value to position the annotation above the bar
            )
