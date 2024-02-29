<template>
    <VContainer>
        <VResponsive>
            <VRow>
                <VCol cols="3">
                    <VSheet>
                        <VSlider class="slider" direction="vertical" color="#4CAF50" show-ticks="always" height="250" track-size="50" thumb-label="always" label="Height (in)"></VSlider>
                    </VSheet>
                </VCol>
                <VCol>
                    <VSheet>
                        <figure class="highcharts-figure">
                            <div id="container_1"></div>
                        </figure>
                    </VSheet>
                </VCol>
            </VRow>
            <VRow>
                <VCol cols="8">
                    <figure class="highcharts-figure">
                        <div id="container_3"></div>
                    </figure>
                </VCol>
                <VCol cols="4" fluid>         
                    <VSheet>
                        <VCard title="Water Level" subtitle="Capacity Remaining" variant="tonal" color="primary" rounded="lg"  align="center">
                            <div id="fluid-meter" ></div>

                        </VCard>
                    </VSheet>
                </VCol>
            </VRow>
        </VResponsive>
    </VContainer>
    </template>
    
    <script setup>
    // IMPORTS
    import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
    import { useRoute ,useRouter } from "vue-router";
    import { useMqttStore} from "@/store/mqttStore";
    import {storeToRefs} from "pinia";
    import {useAppStore} from "@/store/appStore";
    import Highcharts from "highcharts";
    import more from "highcharts/highcharts-more";
    import exporting from "highcharts/modules/exporting";
    more(Highcharts);
    exporting(Highcharts);
    
    
    
    
    // VARIABLES
    const router      = useRouter();
    const route       = useRoute(); 
    const Mqtt        = useMqttStore();
    const appStore    = useAppStore();
    const {payload, payloadTopic} = storeToRefs(Mqtt);
    const Water_r = ref(null);
    const Gauge = ref(null);
    var fm = new FluidMeter();
   
   
    const Water_Height = computed(()=>{
        if(!!payload.value){
      return "${payload.value.Water_Height.toFixed(2)} inches";
    }});

    const reserve= computed(()=>{
    if(!!payload.value){
      return '${payload.value.reserves.toFixed(2)} gallons';
    }});

    const percent= computed(()=>{
    if(!!payload.value){
      return '${payload.value.percent.toFixed(2)} gallons';
    }});



    
    // WATCHERS
    watch(payload,(data)=> { 
     if(Water_r.value.series[0].points.value > 550){ Water_r.value.series[0].points.value -- ; }
        else{ shift.value = true; }
    
    slider.value = data.radar
    
    if (data.Water_Height >= 77) {
      fm.setPercentage(100);
     
      Water_r.value.series[0].addPoint({ y: parseFloat(data.Water_Height.toFixed(2)), x: data.timestamp*1000 }, true, shift.values); 
      Gauge.value.series[0].points[0].update(1000);
    }
    else if (data.water_height <= 0) {
      fm.setPercentage(0);
      Water_r.value.series[0].addPoint({ y: 0, x: data.timestamp*1000 }, true, shift.values); 
      Gauge.value.series[0].points[0].update(0); // Add new data point

    }
    else{
      fm.setPercentage(data.percent.toFixed(2));
      Water_r.value.series[0].addPoint({ y: parseFloat(data.Water_Height.toFixed(2)), x: data.timestamp*1000  }, true, shift.values); 
      Gauge.value.series[0].points[0].update(parseFloat(data.reserve.toFixed(2)));}    

      console.log(data.percent);
      if (data.percent > 98 || data.percent < 2) {
          isActive.value = true;
        } else {
          isActive.value = false;
        } 
    });

    
    // FUNCTIONS
    onMounted(()=>{
      // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
      CreateChart();
      Mqtt.connect();

      setTimeout(()=>{
        Mqtt.subscribe("620156117");
        Mqtt.subscribe("620156117_sub");
      },3000);
    });



    const CreateChart= async()=>{
        Water_r.value=Highcharts.chart("container_1",{
            title:{text:"Water Reserves (10 mins)", align:"left"},
            tooltip:{shared: true},
            chart:{zoomType:"x"},
            yAxis: {
                title:{text: "Water Level"},
                labels:{format: '{value} Gal'},
                min: 0,
                max:1000
            },
            xAxis: {
                title:{text:"Time"},
                type:"datetime"
            },
            series:[{name:"Water",
                type:"area"}]
        });
        Gauge.value=Highcharts.chart("container_3",{
            title: { text: 'Water Reserves', align: 'left'},
            // the value axis
            yAxis: {
            min: 0,
            max: 1000,
            tickPixelInterval: 72,
            tickPosition: 'inside',
            tickColor: Highcharts.defaultOptions.chart.backgroundColor || '#FFFFFF',
            tickLength: 20,
            tickWidth: 2,
            minorTickInterval: null,
            labels: { distance: 20, style: { fontSize: '14px' } },
            lineWidth: 0,
            plotBands: [{ from: 0, to: 200, color: '#DF5353', thickness: 20 }, { from: 200, to: 600, color: '#DDDF0D', thickness: 20
            }, { from: 600, to: 1000, color: '#55BF3B', thickness: 20 }]
            },
            tooltip: { shared:true, },
            pane: { startAngle: -90, endAngle: 89.9, background: null, center: ['50%', '75%'], size: '110%' },
            series: [{
            type:'gauge',
            name: 'Water Capacity',
            data:[0],
            tooltip: { valueSuffix: ' Gal' },
            dataLabels: { format: '{y} Gal', borderWidth: 0, color: ( Highcharts.defaultOptions.title &&
            Highcharts.defaultOptions.title.style && Highcharts.defaultOptions.title.style.color ) || '#333333', style: { fontSize: '16px' } 
            },
            dial: { radius: '80%', backgroundColor: 'gray', baseWidth: 12, baseLength: '0%', rearLength: '0%' },
            pivot: { backgroundColor: 'gray', radius: 6 }
            }]
        });

        
        fm.init({
        targetContainer: document.getElementById("fluid-meter"),
        fillPercentage: percent,
        options: {
            fontSize: "70px",
            fontFamily: "Arial",
            fontFillStyle: "white",
            drawShadow: true,
            drawText: true,
            drawPercentageSign: true,
            drawBubbles: true,
            size: 300,
            borderWidth: 25,
            backgroundColor: "#e2e2e2",
            foregroundColor: "#fafafa",
            foregroundFluidLayer: {
            fillStyle: "purple",
            angularSpeed: 100,
            maxAmplitude: 12,
            frequency: 30,
            horizontalSpeed: -150
            },
            backgroundFluidLayer: {
            fillStyle: "pink",
            angularSpeed: 100,
            maxAmplitude: 9,
            frequency: 30,
            horizontalSpeed: 150
            }
        }
        });
    }

    

    
    onBeforeUnmount(()=>{
      // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
      Mqtt.unsubcribeAll();
    });
    
    </script>
    
    <style scoped>
    /** CSS STYLE HERE */
    
    </style>