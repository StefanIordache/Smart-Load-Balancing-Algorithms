function popStatisticsModal(simulation) {


    $('#modalStatistics').modal('show');

    //cpuLoadsChart();

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