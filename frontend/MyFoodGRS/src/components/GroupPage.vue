<template class>
  <div v-if="!endOfSession" class="scroll">
    <div v-show="!groupActive" class="scroll">
      <div class="q-pa-md q-gutter-sm" v-if="deleteDialog">
        <q-dialog v-model="confirm" persistent>
          <q-card>
            <q-card-section class="row items-center" align="left">
              <q-avatar
                icon="perm_identity"
                :color="userColor"
                text-color="white"
              />
              <span class="q-ml-sm">{{ deleteMassage }}</span>
            </q-card-section>

            <q-card-actions align="left">
              <q-btn
                flat
                label="Cancel"
                color="primary"
                v-close-popup
                @click="cancelDeleting()"
              />
              <q-btn
                flat
                label="Delete"
                color="red"
                v-close-popup
                v-if="deletePossible"
                @click="finishDeleting(userColor)"
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>
      <div v-if="memberCounter > 1" class="groupInfoText">
        <q-input
          filled
          bottom-slots
          v-model="memberName"
          label="Name"
          class="inputBox"
        >
          <template v-slot:hint>
            Max number of friends to add 5, remained {{ memberCounter - 1 }}
          </template>
          <template v-slot:append>
            <q-btn round flat icon="add" @click="submitUser(memberCounter)" />
          </template>
        </q-input>
      </div>
      <br />
      <q-list
        bordered
        class="rounded-borders"
        style="max-width: 98%; margin: auto"
      >
        <div v-for="(value, name, index) in groupMembers" :key="name">
          <q-item class="memberList">
            <q-item-section avatar top>
              <q-icon
                name="perm_identity"
                :color="value[0] === 'organizer' ? 'blue' : value[0]"
                size="34px"
              />
            </q-item-section>

            <q-item-section top>
              <div v-if="!editableForm[index]">
                <q-item-label lines="1">
                  <span class="text-weight-medium">{{ value[1] }}</span>
                </q-item-label>
                <q-item-label caption lines="1">
                  Role:
                  {{
                    value[0] === "organizer" ? "Organizer" : "Companion"
                  }}</q-item-label
                >
              </div>
              <div v-else>
                <q-input v-model="editText" :label="value[0]" dense="dense" />
              </div>
              <q-item-label
                lines="1"
                class="q-mt-xs text-body2 text-weight-bold text-primary text-uppercase"
              >
              </q-item-label>
            </q-item-section>

            <q-item-section top side>
              <div class="text-grey-8 q-gutter-xs">
                <q-btn
                  v-if="editableVisibility[index]"
                  size="12px"
                  flat
                  round
                  icon="edit"
                  @click="editMember(index)"
                />
                <q-btn
                  v-else
                  size="12px"
                  flat
                  round
                  icon="done"
                  :color="editText.length === 0 ? 'red' : 'green'"
                  @click="updateUser(name, index)"
                />
                <q-btn
                  size="12px"
                  flat
                  round
                  icon="delete"
                  @click="deleteUser(name, index, value[1])"
                />
              </div>
            </q-item-section>
          </q-item>
          <q-separator />
        </div>
      </q-list>
    </div>
    <div v-show="!mapActive" class="scroll">
      <div class="q-pa-md q-gutter-sm" v-if="mapDialogActive">
        <q-dialog v-model="confirm" persistent>
          <q-card align="left">
            <q-card-section class="row items-center" align="left">
              <q-avatar
                icon="perm_identity"
                :color="userColor"
                text-color="white"
              />
              <span class="q-ml-sm" align="right">{{ mapMassage }}</span>
            </q-card-section>

            <q-card-actions align="right">
              <q-btn
                flat
                label="Ok"
                color="primary"
                v-close-popup
                @click="mapDialogActive = !mapDialogActive"
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </div>
      <q-btn-dropdown
        split
        disable-main-btn
        class="glossy"
        color="primary"
        :label="cityLabel"
        icon="place"
        style="margin: 5px auto; width: 100%"
      >
        <q-list>
          <q-item clickable v-close-popup @click="selectCity('bolzano')">
            <q-item-section avatar>
              <q-avatar
                icon="location_city"
                color="primary"
                text-color="white"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>Bolzano</q-item-label>
            </q-item-section>
          </q-item>

          <q-item clickable v-close-popup @click="selectCity('trento')">
            <q-item-section avatar>
              <q-avatar
                icon="location_city"
                color="secondary"
                text-color="white"
              />
            </q-item-section>
            <q-item-section>
              <q-item-label>Trento</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <q-banner
        class="bg-primary text-white"
        style="width: 100%; margin-top: 5px"
      >
        Enter your location
      </q-banner>
      <div v-for="(value, name, index) in groupMembers" :key="name">
        <q-input
          filled
          bottom-slots
          v-model="memberlocation[index]"
          :label="value[1]"
          class="inputBox"
        >
          <template v-slot:append>
            <q-btn
              type="submit"
              round
              flat
              icon="place"
              @click="setLocation(value, name, index, memberlocation[index])"
            />
          </template>
        </q-input>
      </div>
      <q-banner
        class="bg-primary text-white"
        style="width: 100%; margin-top: 5px"
      >
        Select your location on map
      </q-banner>
      <div class="map" id="map">
        <GMapMap :center="center" :zoom="zoom" map-type-id="terrain">
          <GMapMarker
            v-for="(marker, index) in markers.slice(
              0,
              Object.keys(this.groupMembers).length
            )"
            :key="index"
            :position="marker.position"
            :clickable="true"
            :draggable="true"
            :icon="getIcon(Object.keys(this.groupMembers)[index])"
            @click="center = position"
            @dragend="
              handleClick($event, Object.keys(this.groupMembers)[index])
            "
          >
          </GMapMarker>
        </GMapMap>
      </div>
    </div>
    <div v-show="!prefActive">
      <div v-for="(value, name, index) in groupMembers" :key="name">
        <div class="q-pa-md">
          <q-list bordered class="rounded-borders" style="border-width: 0">
            <q-expansion-item>
              <div id="q-app">
                <div class="q-pa-md">
                  <div class="q-gutter-md row">
                    <q-select
                      filled
                      dense
                      use-input
                      hide-dropdown-icon
                      v-model="model"
                      :options="foodCategoryObjName"
                      @filter="filterFn"
                      hint="Search for specific dish"
                      style="width: 95%; padding-bottom: 32px; margin-top: 10px"
                      label="Dish"
                      behavior="menu"
                      @popup-hide="submitDish(value, name, searchInput)"
                    >
                      <q-icon name="search" size="20px" />
                      <template v-slot:no-option>
                        <q-item>
                          <q-item-section class="text-grey">
                            No results
                          </q-item-section>
                        </q-item>
                      </template>
                    </q-select>
                  </div>
                </div>
              </div>
              <template v-slot:header>
                <q-item-section avatar>
                  <q-avatar
                    icon="perm_identity"
                    :color="memberColordelete[index]"
                    text-color="white"
                  />
                </q-item-section>

                <q-item-section>
                  Add {{ value[1] }} preferences
                </q-item-section>

                <q-item-section side>
                  <div class="row items-center">
                    <q-icon
                      name="lunch_dining"
                      :color="memberColordelete[index]"
                      size="24px"
                    />
                  </div>
                </q-item-section>
              </template>
              <q-card>
                <div class="q-pa-md row items-start q-gutter-md">
                  <div
                    v-for="(food, indexInner) in foodsCategory"
                    :key="indexInner"
                  >
                    <q-card
                      :class="
                        isInArray(food, memberPreference[name])
                          ? categoryCardColor[index + 1]
                          : categoryCardColor[0]
                      "
                      @click="addPreferences(name, food)"
                    >
                      <q-card-section> {{ food }} </q-card-section>
                    </q-card>
                  </div>
                </div>
              </q-card>
            </q-expansion-item>
          </q-list>
        </div>
      </div>
    </div>
    <div class="footer">
      <q-layout
        view="lHh lpr lFf"
        container
        style="height: 70px"
        class="shadow-2 rounded-borders"
      >
        <q-header elevated>
          <q-tabs>
            <q-tab
              name="Members"
              label="Members"
              icon="group"
              @click="determinePage('member')"
              :class="{ groupActive: groupActive }"
            />
            <q-tab
              name="Preferences"
              label="Preferences"
              icon="restaurant"
              @click="determinePage('pref')"
              :class="{ prefActive: prefActive }"
            />
            <q-tab
              name="Map"
              label="Map"
              icon="map"
              @click="determinePage('map')"
              :class="{ mapActive: mapActive }"
            />
          </q-tabs>
        </q-header>
      </q-layout>
    </div>
  </div>
  <div v-else>
    <div class="no-tasks absolute-center text-h5 text-primary text-center">
      Thank you for participating in our user study.
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
export default {
  props: ["groupInfo"],
  data() {
    return {
      options: [],
      searchLabel: "Search for dish",
      searchInput: "",
      foodCategoryObj: require(`../assets/food_category.json`),
      foodCategoryObjDefault: require(`../assets/food_category.json`),
      foodCategoryObjName: [],
      foodCategoryObjNameDefault: [],
      memberPreference: {},
      categoryCardColor: [
        "my-card",
        "my-card bg-blue text-white",
        "my-card bg-green text-white",
        "my-card bg-purple text-white",
        "my-card bg-red text-white",
        "my-card bg-yellow text-white",
      ],
      foodsCategory: [
        "PASTA",
        "CARNE",
        "RISO",
        "PIZZA",
        "SALUMI",
        "PESCE",
        "FUNGHI",
        "FORMAGGI",
      ],
      color: ref("cyan"),
      memberlocation: ["", "", "", "", ""],
      cityLabel: "Select your city",
      zoom: 13,
      center: { lat: 46.4985, lng: 11.3507 },
      markers: [
        {
          position: {
            lat: 46.4985,
            lng: 11.3507,
          },
        },
        {
          position: {
            lat: 46.4985,
            lng: 11.3507,
          },
        },
        {
          position: {
            lat: 46.4985,
            lng: 11.3507,
          },
        },
        {
          position: {
            lat: 46.4985,
            lng: 11.3507,
          },
        },
        {
          position: {
            lat: 46.4985,
            lng: 11.3507,
          },
        }, // Along list of clusters
      ],
      deletedCount: 0,
      deletedColors: [],
      model: ref(null),
      mapDialogActive: false,
      mapMassage: "",
      deletePossible: true,
      userColor: "",
      deleteMassage: "",
      confirm: "",
      deletingId: -1,
      deleteDialog: false,
      editText: "",
      editableForm: [false],
      editableVisibility: [true],
      memberName: "",
      subpage: "pref",
      prefActive: true,
      mapActive: true,
      groupActive: false,
      memberCounter: 5,
      groupMembers: this.groupInfo,
      memberColor: ["green", "purple", "red", "yellow"],
      memberColordelete: ["blue", "green", "purple", "red", "yellow"],
      endOfSession: false,
    };
  },
  methods: {
    submitDish(value, name) {
      const food = this.foodCategoryObj[this.model];
      this.addPreferences(name, food, value);
      this.model = ref(null);
      this.foodCategoryObjName = this.foodCategoryObjNameDefault;
    },
    filterFn(val, update) {
      if (val.length < 1) {
        this.foodCategoryObjName = this.foodCategoryObjNameDefault;
      } else {
        this.searchInput = "";
        this.searchInput = val;
        update(() => {
          this.filteredList();
        });
      }
      return;
    },
    filteredList() {
      if (this.searchInput === "") {
        this.foodCategoryObjName = this.foodCategoryObjNameDefault;
      } else {
        this.foodCategoryObjName = this.foodCategoryObjName.filter((food) =>
          food.toLowerCase().includes(this.searchInput.toLowerCase())
        );
      }
    },
    determinePage(page) {
      this.subpage = page;
      if (page === "pref") {
        this.prefActive = false;
        this.mapActive = true;
        this.groupActive = true;
      } else if (page === "map") {
        this.prefActive = true;
        this.mapActive = false;
        this.groupActive = true;
      } else {
        this.prefActive = true;
        this.mapActive = true;
        this.groupActive = false;
      }
    },

    submitUser(membercount) {
      var user_default = {
        first_name: "Organizer",
        last_name: "string",
        email: "string",
        latitude: 0,
        longitude: 0,
        role: "companion",
        group_id: 0,
      };
      var url = "http://46.18.25.97:8050/users/companion";
      var request = "POST";
      var user_temp_object = user_default;
      if (this.memberName.length > 0) {
        user_temp_object["first_name"] = this.memberName;
      } else {
        user_temp_object["first_name"] = "Companion" + String(6 - membercount);
      }
      user_temp_object["group_id"] = JSON.parse(
        sessionStorage.getItem("group_id")
      );
      var data = JSON.stringify(user_temp_object);
      if (this.deletedCount > 0) {
        var colorOfNewUser = this.deletedColors.shift();
        this.sendRequest(url, request, data, colorOfNewUser, "insert");
        this.deletedCount--;
      } else {
        this.sendRequest(
          url,
          request,
          data,
          this.memberColor[5 - this.memberCounter],
          "insert"
        );
        this.memberCounter = this.memberCounter - 1;
        this.editableVisibility.push(true);
        this.editableForm.push(false);
      }
    },

    sendRequest(url, request, data, role, type, userId) {
      const headers = {
        "Content-Type": "application/json",
      };
      var data_temp = JSON.parse(data);
      var temp_user_id = "";
      var role_name = role + "_name";
      var first_name = data_temp["first_name"];
      if (request === "POST") {
        axios
          .post(url, data, {
            headers: headers,
          })
          .then((response) => {
            if (type === "update") {
              var temp_user_id = userId;
              this.editText = "";
              this.groupMembers[temp_user_id][1] = first_name;
            } else {
              temp_user_id = JSON.parse(response.data)["user_id"];
              this.memberName = "";
              sessionStorage.setItem(role, temp_user_id);
              sessionStorage.setItem(role_name, first_name);
              this.groupMembers[temp_user_id] = [role, first_name];
              var temp_element_to_add = {};
              temp_element_to_add["id"] = temp_user_id;
              temp_element_to_add["name"] = first_name;
              temp_element_to_add["show"] = true;
              this.memberPreference[temp_user_id] = [];
              return temp_user_id;
            }
          });
      }
    },

    editMember(index) {
      this.editableForm[index] = true;
      this.editableVisibility[index] = false;
    },
    updateUser(userId, index) {
      var user_temp_object = {
        first_name: "Organizer",
        last_name: "string",
        email: "string",
        latitude: 0,
        longitude: 0,
        role: "organizer",
        group_id: 0,
      };
      const user_id = userId;
      var url =
        "http://46.18.25.97:8050/users/update/organizer/" + user_id.toString();
      var request = "POST";
      user_temp_object["first_name"] = this.editText;
      if (index === 0) {
        var role = "organizer";
      } else {
        var role = "companion";
      }
      var data = JSON.stringify(user_temp_object);
      this.sendRequest(url, request, data, role, "update", user_id);
      this.editableForm[index] = false;
      this.editableVisibility[index] = true;
    },
    deleteUser(userId, index, name) {
      this.deleteDialog = true;
      if (index === 0) {
        this.deleteMassage = "Impossible to delete the organizer of the group.";
        this.deletePossible = false;
        this.userColor = this.memberColordelete[index];
        this.deletingId = userId;
      } else {
        this.deleteMassage = "Are you sure you want to delete " + name + "?";
        this.deletePossible = true;
        this.userColor = this.memberColordelete[index];
        this.deletingId = userId;
      }
    },

    finishDeleting(color) {
      this.memberCounter++;
      this.deletedCount++;
      if (color === "green") {
        this.deletedColors.push("green");
      }
      if (color === "purple") {
        this.deletedColors.push("purple");
      }
      if (color === "red") {
        this.deletedColors.push("red");
      } else {
        this.deletedColors.push("yellow");
      }
      var url =
        "http://46.18.25.97:8050/users/companion/delete/" +
        this.deletingId.toString();
      axios.delete(url).then(delete this.groupMembers[this.deletingId]);
      this.deleteDialog = false;
    },
    handleClick(par, userId) {
      var userObj = {
        last_name: "string",
        email: "string",
        latitude: par.latLng.lat(),
        longitude: par.latLng.lng(),
        group_id: 0,
        first_name: "Companion",
        role: "companion",
      };
      var url = "http://46.18.25.97:8050/users/location/" + String(userId);
      axios.post(url, userObj).then(() => {
        sessionStorage.setItem("location", true);
      });
    },
    getIcon(userId) {
      var role = this.groupInfo[userId][0];
      if (role === "organizer") {
        return require("../assets/markerBlue.png");
      } else if (role === "green") {
        return require("../assets/markerGreen.png");
      } else if (role === "purple") {
        return require("../assets/markerPurple.png");
      } else if (role === "red") {
        return require("../assets/markerRed.png");
      }
      if (role === "yellow") {
        return require("../assets/markerYellow.png");
      }
    },
    selectCity(city) {
      if (city === "trento") {
        this.cityLabel = "Trento";
        this.center = { lat: 46.066669, lng: 11.11907 };
        this.zoom = 12;
        this.markers = [
          {
            position: {
              lat: 46.066669,
              lng: 11.11907,
            },
          },
          {
            position: {
              lat: 46.066669,
              lng: 11.11907,
            },
          },
          {
            position: {
              lat: 46.066669,
              lng: 11.11907,
            },
          },
          {
            position: {
              lat: 46.066669,
              lng: 11.11907,
            },
          },
          {
            position: {
              lat: 46.066669,
              lng: 11.11907,
            },
          }, // Along list of clusters
        ];
      } else {
        this.cityLabel = "Bolzano";
      }
    },
    setLocation(value, name, index, memberLoc) {
      const headers = {
        "Content-Type": "application/json",
      };
      var addressToSend = {
        address: "",
      };
      if (memberLoc.length > 0) {
        if (this.cityLabel === "Bolzano" || this.cityLabel === "Trento") {
          addressToSend["address"] =
            memberLoc + ", " + this.cityLabel + ", Italy";
          var addressObject = JSON.stringify(addressToSend);
          var url = "http://46.18.25.97:8050/users/location/address/" + name;
          axios
            .post(url, addressObject, {
              headers: headers,
            })
            .then((response) => {
              var coordincation = JSON.parse(response.data);
              var objectKey = Object.keys(coordincation);
              const lat = parseFloat(coordincation[objectKey]["lat"]);
              const lon = parseFloat(coordincation[objectKey]["lon"]);
              this.markers[index] = {
                position: {
                  lat: lat,
                  lng: lon,
                },
              };
              sessionStorage.setItem("location", true);
            });
        } else {
          this.mapDialogActive = true;
          this.mapMassage = "Please select your city";
        }
      } else {
        this.mapDialogActive = true;
        this.mapMassage = "Please enter your street name";
      }
    },
    addPreferences(user_id, food, name) {
      const headers = {
        "Content-Type": "application/json",
      };
      var preference_template = {
        user_id: 0,
        PASTA: this.memberPreference[user_id].includes("PASTA"),
        CARNE: this.memberPreference[user_id].includes("CARNE"),
        PIZZA: this.memberPreference[user_id].includes("PIZZA"),
        TORTELLINI: this.memberPreference[user_id].includes("TORTELLINI"),
        SALUMI: this.memberPreference[user_id].includes("SALUMI"),
        PESCE: this.memberPreference[user_id].includes("PESCE"),
        LEGUMI: this.memberPreference[user_id].includes("LEGUMI"),
        FUNGHI: this.memberPreference[user_id].includes("FUNGHI"),
        CROSTACEI_E_MOLLUSCHI: this.memberPreference[user_id].includes(
          "CROSTACEI_E_MOLLUSCHI"
        ),
        VERDURE: this.memberPreference[user_id].includes("VERDURE"),
        GNOCCHI: this.memberPreference[user_id].includes("GNOCCHI"),
        INTERIORA: this.memberPreference[user_id].includes("INTERIORA"),
        FORMAGGI: this.memberPreference[user_id].includes("FORMAGGI"),
        RISO: this.memberPreference[user_id].includes("RISO"),
      };
      confirm;
      var url = "http://46.18.25.97:8050/preferences";
      preference_template[food] = !preference_template[food];
      preference_template.user_id = parseInt(user_id);
      axios
        .post(url, JSON.stringify(preference_template), {
          headers: headers,
        })
        .then();
      var tempArray = this.memberPreference[user_id];
      if (!this.memberPreference[user_id].includes(food)) {
        tempArray.push(food);
      } else {
        const index = tempArray.indexOf(food);
        tempArray.splice(index, 1);
      }
      this.memberPreference[user_id] = tempArray;
    },
    isInArray(element, array) {
      if (typeof array !== "undefined") {
        if (array.includes(element)) {
          return true;
        } else {
          return false;
        }
      } else {
        return false;
      }
    },
  },
  mounted() {
    if (String(sessionStorage.getItem("Selected")) === "true") {
      this.endOfSession = true;
    } else {
      this.endOfSession = false;
    }
    const url =
      "http://46.18.25.97:8050/preferences/" +
      JSON.parse(sessionStorage.getItem("group_id"));
    axios.get(url).then((response) => {
      if (typeof response.data !== "undefined") {
        this.memberPreference = response.data;
      }
    });
    this.foodCategoryObjName = Object.keys(this.foodCategoryObj);
    this.foodCategoryObjNameDefault = Object.keys(this.foodCategoryObjDefault);
    this.options = this.foodCategoryObjName;
  },
};
</script>

<style scoped>
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
}
.prefActive {
  background: rgb(218, 218, 232);
}
.mapActive {
  background: rgb(218, 218, 232);
}
.groupActive {
  background: rgb(218, 218, 232);
}
.inputBox {
  padding: 3px;
  margin: 10px;
}
.groupInfoText {
  margin-bottom: 10px;
}
#map {
  align-items: center;
  justify-content: center;
  justify-content: center;
  align-items: center;
  height: 200px;
  margin-left: auto;
  margin-right: auto;
}
.map {
  margin-top: 10px;
  overflow: hidden;

  padding-bottom: 0;

  position: relative;

  height: 0;
}

.map iframe {
  left: 0;

  top: 0;

  height: 100%;

  width: 100%;

  position: absolute;
}
.scroll {
  margin-bottom: 70px;
}
</style>
