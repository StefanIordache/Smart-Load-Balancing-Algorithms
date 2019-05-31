function popResultsModal(simulation) {


    $('#modalStatistics').modal('show');

    console.log(simulation);

    //cpuLoadsChart();
    let snapshots_count = -1;
    getNumberOfSnapshotsAsync(simulation).then(function(result_count) {
        snapshots_count = result_count.data;
        console.log(snapshots_count);

        for (i = 0; i < snapshots_count; i++) {
            getSnapshotsByIndexAsync(simulation, i).then(function(result_snapshots) {
               console.log(result_snapshots.data)
            });
        }
    });

}

/*
 CPU Usage Chart
 */
function cpuLoadsChart() {

    am4core.useTheme(am4themes_frozen);
    am4core.useTheme(am4themes_animated);

    // Create chart instance
    var cpuChart = am4core.create("chartCPULoads", am4charts.XYChart);

    // Increase contrast by taking evey second color
    cpuChart.colors.step = 2;

    // Add data
    cpuChart.data = generateChartData(params);

    // Create axes
    var timelineAxis = cpuChart.xAxes.push(new am4charts.ValueAxis());
    timelineAxis.renderer.minGridDistance = 50;

    // Create series
    var series = cpuChart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "ceva";
    series.dataFields.dateX = "altceva";

    // Add scrollbar
    cpuChart.scrollbarX = new am4charts.XYChartScrollbar();
    cpuChart.scrollbarX.series.push(series);


    function generateChartData(params) {

    }
}

async function getNumberOfSnapshotsAsync(simulation) {
    let result = await axios.get('/get_snapshots_counter_by_simulation_id', {
        params: {
            simulation_id: simulation.id
        }
    });

    return result;
}

async function getSnapshotsByIndexAsync(simulation, index) {
    let result = await axios.get('/get_snapshots_json_by_simulation_id_and_index', {
        params: {
            simulation_id: simulation.id,
            index: index
        }
    });

    return result;
}