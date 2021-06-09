var data = {
	labels: ["1", "2", "3", "4", "5", "6", "7"],
	datasets: [
		{
			label: "",
			backgroundColor: "rgba(179,181,198,0.2)",
			borderColor: "rgba(179,181,198,1)",
			pointBackgroundColor: "rgba(179,181,198,1)",
			pointBorderColor: "#fff",
			pointHoverBackgroundColor: "#fff",
			pointHoverBorderColor: "rgba(179,181,198,1)",
			data: [0, 2, 4, 6, 10]
		},
	]
};
var ctx = document.getElementById("myChart");
var options = {
	tooltips: {
		mode: 'label',
		callbacks: {
			label: tooltipItem => `${tooltipItem.yLabel}: ${tooltipItem.xLabel}`,
			title: () => null,
		}
	},
	legend: {
		display: false,
	},
	scales: {
		yAxes: [{
			display: false,
			gridLines: {
				display: false
			}
		}]
	}
};
var myRadarChart = new Chart(ctx, {
	type: 'radar',
	data: data,
	options: options,
});
