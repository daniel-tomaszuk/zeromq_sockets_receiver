const legendNames = [];

function createTimeline() {
        let cpu = {};
        let mem = {};

        const cpuChartPops = {
            responsive: true,
            enableDpiScaling: false,
            millisPerPixel: 100,
            grid: {
                millisPerLine: 4000,
                fillStyle: '#fff',
                strokeStyle: 'rgba(0, 0, 0, 0.08)',
                verticalSections: 10,
            },
            labels: {
                fillStyle: '#000',
                fontSize: 18
            },
            timestampFormatter: SmoothieChart.timeFormatter,
            maxValue: 10,  // only 10% so it's easier to see small values
            minValue: 0
        };

        const memChartPops = {
            responsive: true,
            enableDpiScaling: false,
            millisPerPixel: 100,
            grid: {
                millisPerLine: 4000,
                fillStyle: '#fff',
                strokeStyle: 'rgba(0, 0, 0, 0.08)',
                verticalSections: 10,
            },
            labels: {
                fillStyle: '#000',
                fontSize: 18
            },
            timestampFormatter: SmoothieChart.timeFormatter,
            maxValue: 100, // in MB
            minValue: 0
        };


        let cpuChart = new SmoothieChart(cpuChartPops);
        let memChart = new SmoothieChart(memChartPops);

        function add_timeseries(obj, chart, color) {
            obj[color] = new TimeSeries();
            chart.addTimeSeries(obj[color], {
                strokeStyle: color,
                lineWidth: 4
            })
        }

        let evtSource = new EventSource("http://localhost:8000/feed");
        evtSource.onmessage = function(event) {
            let eventData = JSON.parse(event.data);

            if (!(eventData.color in cpu)) {
                add_timeseries(cpu, cpuChart, eventData.color);
            }
            if (!(eventData.color in mem)) {
                add_timeseries(mem, memChart, eventData.color);
            }
            cpu[eventData.color].append(
                Date.parse(eventData.timestamp), eventData.cpu
            )
            mem[eventData.color].append(
                Date.parse(eventData.timestamp), eventData.mem
            )

            fillLegend(eventData.color, eventData.app_name);
        };

        cpuChart.streamTo(
            document.getElementById("cpu-chart"), 1000
        );
        memChart.streamTo(
            document.getElementById("mem-chart"), 1000
        )
    }

function fillLegend(color, name) {

    let legendColorElement = `<div class='square' style="background: ${color}"></div>`;
    const legendTable = $(".legend");
    if (!(legendNames.includes(name))) {
        legendTable.append(`
            <tr>
                <td>${legendColorElement}</td>
                <td>${name}</td>
            </tr>
        `)
        legendNames.push(name);
    }
}
