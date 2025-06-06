import { boot } from "quasar/wrappers";
import VueGoogleMaps from "@fawmi/vue-google-maps";

export default boot(({ app }) => {
  app.use(VueGoogleMaps, {
    load: {
      key: "AIzaSyBVKguW-Fc_dQM2CmrmKFQw4FtTTlw6mdw",
    },
  });
});
