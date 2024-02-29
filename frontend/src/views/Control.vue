<template>
    <VContainer>
        <VResponsive>
            <VCol cols="12" align="center">
                <VCard title="Combination" align="center">
                    <p>Enter your four(4) digit passcode</p>
                    <v-otp-input v-model="passcode" length="4"></v-otp-input>
                </VCard>
                <VBtn @click= "Submit_date();" color="primary" text="Submit"></VBtn>
            </VCol>
        </VResponsive>
    </VContainer>    
    </template>
    
    <script setup>
    // IMPORTS
    import { useMqttStore } from "@/store/mqttStore";
    import { useAppStore } from "@/store/appStore";
    import { ref,reactive,watch ,onMounted,onBeforeUnmount,computed } from "vue";  
    import { useRoute ,useRouter } from "vue-router";
    
    
    
    // VARIABLES
    const router      = useRouter();
    const route       = useRoute(); 
    const passcode    = ref("");
    const mqtt        = useMqttStore();
    const AppStore    = useAppStore();
    
    
    
    
    // COMPUTED PROPERTIES
  
    
    // WATCHERS
    
    
    // FUNCTIONS
    onMounted(()=>{
      // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
      mqtt.connect();
      setTimeout(() => {
      // Subscribe to each topic
      mqtt.subscribe("620156117");
      mqtt.subscribe("620156117_sub");
    }, 3000);
    });
    
    
    onBeforeUnmount(()=>{
      // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
      mqtt.unsubcribeAll();
    });
    
    function Submit_date() {
        if (passcode.value.length == 4){
            console.log(passcode.value);
            AppStore.getpassword(passcode.value);
        }
    
}
    
    </script>
    
    <style scoped>
    /** CSS STYLE HERE */
    
    </style>
    