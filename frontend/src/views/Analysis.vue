<template>
    <VContainer>
        <VResponsive>
            <VRow>
                <VCol cols="3" align="center">
                    <v-text-field label= "Start Date" type= "Date" v-model="start" density= "compact" variant= "solo-inverted" max-width= "300" flat></v-text-field>
                    <v-text-field label= "End Date" type= "Date" v-model="end" density= "compact" variant= "solo-inverted" max-width= "300" flat></v-text-field>
                    <VSpacer></VSpacer>
                    <VBtn  text="Analyze" @click="update();" variant="tonal" rounded="lg"></VBtn>                        
                </VCol>
                <VCol cols="3" height="250">
                    <VCard title="Average" subtitle="for the selected period" width="250" height="200" variant="elevated" rounded="lg" density="compact" align="center">
                        <v-card-item>
                            <span class="text-h1 text-black">
                                {{avg.value }}
                            </span>
                            <small>Gal</small>
                        </v-card-item>
                    </VCard>
                </VCol>
            </VRow>
            <VRow max-width="1200" justify="start">
                <VCol cols="12">
                <figure class="highcharts-figures">
                    <div id="container0"></div>
                </figure>
                </VCol>
                <VCol cols="12">
                    <figure class="highcharts-figures">
                        <div id="container1"></div>
                    </figure>
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
    const router                        = useRouter();
    const route                         = useRoute(); 
    const Mqtt                          = useMqttStore();
    const appStore                      = useAppStore();
    const {payload, payloadTopic}       = storeToRefs(Mqtt);
    const Water_resevere                = ref(null);
    const HeightnWater                  = ref(null);
    var start                           =ref(null);
    var end                             =ref(null);
    var avg                             =reactive({value:0})


    
    
    // COMPUTED PROPERTIES
    const fullname = computed(()=>{    
      return `${firstname.value} ${lastname.value}`;
    });
    
    //WATCHERS
    /*watch(fullname,  (name) => {
      // console.log(name);  
      clearTimeout(nameID); // prevent errant multiple timeouts from being generated
      typing.value = "typing..."
      nameID = setTimeout(() => {typing.value = ""},1000);
    });*/
    
    // FUNCTIONS
    onMounted(()=>{
      // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
      CreateCharts();
      Mqtt.connect();

      setTimeout(() => {
      // Subscribe to each topic
      Mqtt.subscribe("620156117");
      Mqtt.subscribe("620156117_sub");
    }, 3000);
    });
     const CreateCharts = async()=> {
        Water_resevere.value = Highcharts.chart("container0",{
            title:{text:"Water Management Analysis", align:"left"},
            tooltip:{shared: true},
            chart:{zoomType:"x"},
            yAxis: {
                title:{text: "Water Reserve"},
                labels:{format: '{value} Gal'},
                min: 0,
                max:1000
            },
            xAxis: {
                title:{text:"Time"},
                type:"datetime"
            },
            series:[{name:"Reserve",
                type:"line"}]
            });

            HeightnWater.value = Highcharts.chart("container1",{
            title:{text:"Height and Water Level Correlation Analysis", align:"left"},
            tooltip:{shared: true},
            chart:{zoomType:"x"},
            yAxis: {
                title:{text: "Height"},
                labels:{format: '{value} in'},
                min: 0,
                max:100
            },
            xAxis: {
                title:{text:"Water Height"},
                labels:{format: '{value} in'},
                min: 0,
                max:80
            },
            series:[{name:"Analysis",
                type:"scatter"}]
            });
    } 
    
    const update = async () => {
    if (!!start.value && !!end.value) {
      let start_time = new Date(start.value).get_time() / 1000;
      let end_time = new Date(end.value).get_time() / 1000;
      const data = await AppStore.get_data(start_time, end_time);
      const average = await AppStore.get_avg(start_time, end_time);
      let reserve = [];
      data.forEach((row) => {
        reserve.push({
          x: row.timestamp * 1000,
          y: parseFloat(row.reserve.toFixed(2)),
        });
        Water_Height.push({
          x: row.timestamp * 1000,
          y: parseFloat(row.Water_Height.toFixed(2)),
        });        
      });
      Water_resevere.value.series[0].setData(reserve);
      HeightnWater.value.series[0].setData(Water_Height);
      avg.value = average[0].average.toFixed(1)*10; 
      console.log(average);
      console.log(Water_Height);
      console.log(reserve);
    }
  };
  
    
    onBeforeUnmount(()=>{
      // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
      Mqtt.unsubcribeAll();
    });
    
    </script>
    
    <style scoped>
    /** CSS STYLE HERE */
    
    </style>
    