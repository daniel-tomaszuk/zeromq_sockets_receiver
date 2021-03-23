function createTimeline() {
        let cpu = {};
        let mem = {};

        const chartPops = {
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
            maxValue: 100,
            minValue: 0
        };

        let cpu_chart = new SmoothieChart(chartPops);
        let mem_chart = new SmoothieChart(chartPops);

        function add_timeseries(obj, chart, color) {
            obj[color] = new TimeSeries();
            chart.addTimeSeries(obj[color], {
                strokeStyle: color,
                lineWidth: 4
            })
        }

        let evtSource = new EventSource("http://localhost:8000/feed");
        evtSource.onmessage = function(event) {

            console.log("GOT SSE EVENT");
            console.log(event);
            console.log("DATA")
            console.log(event.data)

            let obj = JSON.parse(event.data);




            if (!(obj.color in cpu)) {
                add_timeseries(cpu, cpu_chart, obj.color);
            }
            if (!(obj.color in mem)) {
                add_timeseries(mem, mem_chart, obj.color);
            }
            cpu[obj.color].append(
                Date.parse(obj.timestamp), obj.cpu
            )
            mem[obj.color].append(
                Date.parse(obj.timestamp), obj.mem
            )
        };

        cpu_chart.streamTo(
            document.getElementById("cpu-chart"), 1000
        );
        mem_chart.streamTo(
            document.getElementById("mem-chart"), 1000
        )
    }
