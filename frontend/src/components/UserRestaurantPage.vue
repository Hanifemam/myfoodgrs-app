<template>
  <div v-if="!endOfSession">
    <div v-show="!restPageActive">
      <div :class="{ clear: !popActive }">
        <div v-show="!popActive && pageload">
          <div v-for="(rest, index) in restaurantJson" :key="index">
            <!-- <div v-if="index < maxpagePop"> -->
            <div
              class="q-pa-md row items-start q-gutter-md"
              style="margin: auto"
              :id="JSON.parse(rest).id"
            >
              <q-card class="my-card" style="width: 90%; margin: auto">
                <q-card-section style="padding: 5px">
                  <div class="text-h6 q-mb-xs" @click="goToRestPage(rest)">
                    {{ JSON.parse(rest).name }}
                  </div>
                  <div class="q-pa-md" style="padding: 5px">
                    <div class="q-gutter-y-md column" style="width: 30px">
                      <q-rating
                        v-model="model3[JSON.parse(rest).id]"
                        max="1"
                        size="30px"
                        color="red"
                        color-selected="red-9"
                        icon="favorite_border"
                        icon-selected="favorite"
                        @click="submitRemoveBookmark(JSON.parse(rest).id)"
                      />
                    </div>
                  </div>
                </q-card-section>
                <img
                  :src="getLogo(JSON.parse(rest).logo)"
                  style="height: 200px; padding: 2px; border-radius: 5px"
                  @click="goToRestPage(rest)"
                />
                <q-card-section class="q-pt-none" @click="goToRestPage(rest)">
                  <p>
                    Address: {{ JSON.parse(rest).address }},
                    {{ JSON.parse(rest).city }}, Italy
                  </p>
                </q-card-section>
              </q-card>
            </div>
            <!-- </div> -->
          </div>
          <div class="centering">
            <!-- <div v-if="counterBtn < restaurantJson.length">
              <q-btn
                color="primary"
                label="Show More"
                @click="nextPagePop()"
                style="margin: 10px auto"
              />
            </div>
            <div v-else>
              <q-btn color="grey" label="No More" style="margin: 10px auto" />
            </div> -->
          </div>
          <q-page-scroller
            position="bottom-right"
            :scroll-offset="150"
            :offset="[18, 18]"
          >
            <q-btn
              fab
              icon="keyboard_arrow_up"
              color="primary"
              class="scroll"
            />
          </q-page-scroller>
        </div>
      </div>
      <div v-show="!relActive && pageload">
        <div :class="{ clear: !relActive }">
          <q-page-scroller
            position="bottom-right"
            :scroll-offset="150"
            :offset="[18, 18]"
          >
            <q-btn
              fab
              icon="keyboard_arrow_up"
              color="primary"
              class="scroll"
            />
          </q-page-scroller>
          <div v-if="restaurantJsonRel.length">
            <div v-for="(rest, index) in restaurantJsonRel" :key="index">
              <!-- <div v-if="index < maxpageRel"> -->
              <div
                class="q-pa-md row items-start q-gutter-md"
                style="margin: auto"
              >
                <q-card class="my-card" style="width: 90%; margin: auto">
                  <q-card-section style="padding: 5px">
                    <div class="text-h6 q-mb-xs" @click="goToRestPage(rest)">
                      {{ JSON.parse(rest).name }}
                    </div>
                    <div class="q-pa-md" style="padding: 5px">
                      <div class="q-gutter-y-md column" style="width: 30px">
                        <q-rating
                          v-model="model3[JSON.parse(rest).id]"
                          max="1"
                          size="30px"
                          color="red"
                          color-selected="red-9"
                          icon="favorite_border"
                          icon-selected="favorite"
                          @click="submitRemoveBookmark(JSON.parse(rest).id)"
                        />
                      </div>
                    </div>
                  </q-card-section>
                  <img
                    :src="getLogo(JSON.parse(rest).logo)"
                    style="height: 200px; padding: 2px; border-radius: 5px"
                    @click="goToRestPage(rest)"
                  />
                  <q-card-section class="q-pt-none" @click="goToRestPage(rest)">
                    Address: {{ JSON.parse(rest).address }},
                    {{ JSON.parse(rest).city }}, Italy
                  </q-card-section>
                </q-card>
              </div>
              <!-- </div> -->
            </div>
            <div class="centering">
              <!-- <div v-if="counterBtnRel < restaurantJson.length">
                <q-btn
                  color="primary"
                  label="Show More"
                  @click="nextPageRel()"
                  style="margin: 10px auto"
                />
              </div>
              <div v-else>
                <q-btn color="grey" label="No More" style="margin: 10px auto" />
              </div> -->
            </div>
          </div>
          <div v-else>
            <q-icon
              name="local_dining"
              size="50px"
              color="primary"
              class="absolute-center icon"
            />
            <div
              class="no-tasks absolute-center text-h5 text-primary text-center"
            >
              You have not inserted any preference or there is no recommendation
              with respect to inserted information.
            </div>
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
            <q-tabs class="bg-primary text-white shadow-2">
              <q-tab
                name="Popular"
                label="Popular"
                icon="group"
                @click="determinePage('pop')"
                :class="{ popActive: popActive }"
              />
              <q-tab
                name="Relevance"
                label="Recommendations"
                icon="restaurant"
                @click="determinePage('rel')"
                :class="{ relActive: relActive }"
              />
            </q-tabs>
          </q-header>
        </q-layout>
      </div>
    </div>
    <div v-if="restPageActive">
      <q-btn
        round
        color="primary"
        icon="chevron_left"
        position="top-left"
        @click="scrollToAnchorPoint(JSON.parse(restPageInfo).id)"
        size="0.7em"
        class="button-back"
      />
      <div
        class="card-position q-pa-md row items-start q-gutter-md"
        style="margin: auto"
      >
        <q-card class="my-card" style="width: 90%; margin: auto">
          <q-card-section style="padding: 5px">
            <div class="text-h6 q-mb-xs">
              {{ JSON.parse(restPageInfo).name }}
            </div>
            <div class="q-pa-md" style="padding: 5px">
              <div class="q-gutter-y-md column" style="width: 30px">
                <q-rating
                  v-model="model3[JSON.parse(restPageInfo).id]"
                  max="1"
                  size="30px"
                  color="red"
                  color-selected="red-9"
                  icon="favorite_border"
                  icon-selected="favorite"
                  @click="submitRemoveBookmark(JSON.parse(restPageInfo).id)"
                />
              </div>
            </div>
          </q-card-section>
          <img
            :src="getLogo(JSON.parse(restPageInfo).logo)"
            style="height: 200px; padding: 2px; border-radius: 5px"
          />
          <q-card-section class="q-pt-none">
            <div class="q-pa-md row items-start q-gutter-md">
              <q-card class="my-card">
                <q-card-section>
                  <p>
                    Address: {{ JSON.parse(restPageInfo).address }},
                    {{ JSON.parse(restPageInfo).city }}, Italy
                  </p>
                  <p>
                    <a
                      :href="links[JSON.parse(restPageInfo).name]"
                      style="text-decoration: none"
                      target="_blank"
                      ><b>Link</b></a
                    >
                  </p>
                </q-card-section>
              </q-card>
            </div>
            <div class="q-pa-md row items-start q-gutter-md">
              <q-card class="my-card" style="width: 100%">
                <q-card-section style="width: 100%">
                  <p>
                    Popularity: {{ popularity(JSON.parse(restPageInfo).id) }}
                    <q-linear-progress
                      :value="popularityObj[JSON.parse(restPageInfo).id]"
                      color="red"
                      class="q-mt-sm"
                    />
                  </p>
                  <p>
                    Selected as the final choice:
                    {{ selectedPopularity(JSON.parse(restPageInfo).id) }}
                    <q-linear-progress
                      :value="
                        selectedPopularityObj[JSON.parse(restPageInfo).id]
                      "
                      class="q-mt-sm"
                    />
                  </p>
                </q-card-section>
              </q-card>
            </div>
            <div v-if="restaurantJsonRel.length">
              <div class="q-pa-md row items-start q-gutter-md">
                <q-card class="my-card" style="width: 100%">
                  <q-card-section style="width: 100%">
                    <div
                      v-for="(
                        userAttractiveness, name, index
                      ) in attractiveness"
                      :key="index"
                    >
                      <p>
                        Attractiveness for you:
                        <q-linear-progress
                          :value="
                            userAttractiveness[JSON.parse(restPageInfo).id]
                          "
                          :color="groupInfo[name][0]"
                          class="q-mt-sm"
                        />
                      </p>
                    </div>
                    <div>
                      {{ getSimilarity(JSON.parse(restPageInfo).id) }}
                      Popularity in user like yours:
                      <q-linear-progress
                        :value="similarityValue"
                        color="orange"
                        class="q-mt-sm"
                      />
                    </div>
                  </q-card-section>
                </q-card>
              </div>
            </div>
            <div class="q-pa-md row items-start q-gutter-md">
              <q-card class="my-card" style="width: 100%">
                <q-card-section style="width: 100%">
                  <p v-show="Boolean(JSON.parse(restPageInfo).price_eco)">
                    Price: Economic
                  </p>
                  <div
                    class="parent"
                    v-show="Boolean(JSON.parse(restPageInfo).price_eco)"
                  >
                    <q-btn color="grey" label="$" class="critique-btn" />
                    <q-btn
                      color="primary"
                      label="$$"
                      @click="price('mid')"
                      class="critique-btn"
                    />
                    <q-btn
                      color="primary"
                      label="$$$"
                      @click="price('exp')"
                      class="critique-btn"
                    />
                  </div>
                  <p v-show="Boolean(JSON.parse(restPageInfo).price_mid)">
                    Price: Mid-range
                  </p>
                  <div
                    class="parent"
                    v-show="Boolean(JSON.parse(restPageInfo).price_mid)"
                  >
                    <q-btn
                      color="primary"
                      label="$"
                      @click="price('eco')"
                      class="critique-btn"
                    />
                    <q-btn color="grey" label="$$" class="critique-btn" />
                    <q-btn
                      color="primary"
                      label="$$$"
                      @click="price('exp')"
                      class="critique-btn"
                    />
                  </div>
                  <p v-show="Boolean(JSON.parse(restPageInfo).price_expensive)">
                    Price: Expensive
                  </p>
                  <div
                    class="parent"
                    v-show="Boolean(JSON.parse(restPageInfo).price_expensive)"
                  >
                    <q-btn
                      color="primary"
                      label="$"
                      @click="price('eco')"
                      class="critique-btn"
                    />
                    <q-btn
                      color="primary"
                      label="$$"
                      @click="price('mid')"
                      class="critique-btn"
                    />
                    <q-btn color="grey" label="$$$" class="critique-btn" />
                  </div>
                </q-card-section>
              </q-card>
              <br />

              {{ checkValidity() }}

              <q-card
                v-if="String(locationValidity) === 'true'"
                class="my-card"
                style="width: 100%"
              >
                <q-card-section style="width: 100%">
                  {{ memberDistanceCal(JSON.parse(restPageInfo).id) }}
                  <div v-for="(value, key) in groupInfo" :key="key">
                    {{ value[1] }}'s distance {{ membersDistance[key] }} KM
                  </div>
                  <p></p>
                  <!-- Group's average distance
                  {{ avrDistance(JSON.parse(restPageInfo)) }} KM
                  <p></p> -->
                  <div class="parent">
                    <q-btn
                      color="primary"
                      label="Closer"
                      @click="distance(JSON.parse(restPageInfo))"
                    />
                  </div>
                </q-card-section>
              </q-card>
            </div>
          </q-card-section>

          <q-card-section style="padding-top: 0px">
            <div class="q-pa-md" style="max-width: 350px; padding-top: 0px">
              <q-list bordered class="rounded-borders">
                <q-expansion-item
                  expand-separator
                  icon="restaurant_menu"
                  label="Menu"
                  caption="Menu List"
                >
                  <div
                    v-for="(foodList, category, index) in menuList"
                    :key="index"
                  >
                    <q-expansion-item
                      v-if="foodList.length > 0"
                      :header-inset-level="1"
                      expand-separator
                      :label="
                        food_name_change(category) +
                        ' (' +
                        String(foodList.length) +
                        ')'
                      "
                    >
                      <div class="q-pa-md" style="max-width: 350px">
                        <div v-for="(food, indexIn) in foodList" :key="indexIn">
                          <q-list bordered separator>
                            <q-item clickable v-ripple>
                              <q-item-section>{{ food }}</q-item-section>
                            </q-item>
                          </q-list>
                        </div>
                      </div>
                    </q-expansion-item>
                  </div>
                </q-expansion-item>
              </q-list>
            </div>
          </q-card-section>
        </q-card>
      </div>
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
  props: ["groupInfo", "groupId"],
  data() {
    return {
      selectedPopularityObj: {},
      popularityObj: {},
      endOfSession: false,
      links: require(`../assets/external_link.json`),
      counterBtnRel: 0,
      counterBtn: 0,
      distanceAvr: 0,
      distanceCounter: 0,
      locationValidity: false,
      similarityValue: 0,
      restPageInfo: JSON.stringify({
        id: -1,
        name: "",
        price_eco: -1,
        price_mid: -1,
        price_expensive: -1,
        service_home_delivery: -1,
        latitude: -1,
        longitude: -1,
        address: "",
        city: "",
        logo: "",
      }),
      membersDistance: {},
      maxDistance: 0,
      restPageActive: false,
      maxpagePop: 1,
      maxpageRel: 1,
      pageload: false,
      restaurantJsonRel: {},
      bookmarked: [],
      model: ref(1),
      model3: { "-1": ref(0) },
      subpage: "pop",
      popActive: false,
      relActive: true,
      restaurantJson: {},
      menuList: {},
      group_id_intract: JSON.parse(sessionStorage.getItem("group_id")),
    };
  },
  methods: {
    food_name_change(food_name) {
      if (food_name === "CROSTACEI_E_MOLLUSCHI") {
        return "FASTFOOD";
      }
      if (food_name === "GNOCCHI") {
        return "SOUP";
      }
      if (food_name === "TORTELLINI") {
        return "POLO";
      }
      if (food_name === "LEGUMI") {
        return "NOODLE";
      } else {
        return food_name;
      }
    },
    popularity(restId) {
      var url =
        "http://46.18.25.97:8050/restaurant/popularity/" + String(restId);
      axios.get(url).then((response) => {
        this.popularityObj[restId] = parseFloat(JSON.parse(response.data));
      });
    },
    selectedPopularity(restId) {
      var url =
        "http://46.18.25.97:8050/restaurant/select/popularity/" +
        String(restId);
      axios.get(url).then((response) => {
        this.selectedPopularityObj[restId] = parseFloat(
          JSON.parse(response.data)
        );
      });
    },
    getLogo(logo) {
      return require(`../assets/logo/` + String(logo));
    },
    determinePage(page) {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Recommendation page" + String(page) + "selected",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.subpage = page;
      if (page === "pop") {
        this.popActive = false;
        this.relActive = true;
      } else {
        this.popActive = true;
        this.relActive = false;
      }
    },
    submitRemoveBookmark(restaurantId) {
      if (!this.bookmarked.includes(restaurantId)) {
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Restaurant " + String(restaurantId) + " Booked",
        };
      } else {
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Restaurant " + String(restaurantId) + " Unbooked",
        };
      }
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      var bookmarkObj = {
        restaurant_id: restaurantId,
        group_id: sessionStorage.getItem("group_id"),
      };
      if (!this.bookmarked.includes(restaurantId)) {
        const headers = {
          "Content-Type": "application/json",
        };
        const data = JSON.stringify(bookmarkObj);
        const url = "http://46.18.25.97:8050/bookmarked";
        axios
          .post(url, data, {
            headers: headers,
          })
          .then();
        this.bookmarked.push(restaurantId);
        this.model3[restaurantId] = ref(1);
      } else {
        const headers = {
          "Content-Type": "application/json",
        };
        const data = JSON.stringify(bookmarkObj);
        const url = "http://46.18.25.97:8050/bookmarked/delete";
        axios
          .put(url, data, {
            headers: headers,
          })
          .then();
        const index = this.bookmarked.indexOf(restaurantId);
        this.bookmarked.splice(index, 1);
        this.model3[restaurantId] = ref(0);
      }
    },
    nextPagePop() {
      this.maxpagePop++;
      this.counterBtn++;
    },
    nextPageRel() {
      this.maxpageRel++;
      this.counterBtnRel++;
    },
    goToRestPage(rest) {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Restaurant " + String(rest) + " page visited",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.restPageActive = !this.restPageActive;
      this.restPageInfo = rest;
      const urlmnue =
        "http://46.18.25.97:8050/restaurant/menu/" + JSON.parse(rest).id;
      axios.get(urlmnue).then((response) => {
        this.menuList = JSON.parse(JSON.stringify(response.data));
      });
    },
    scrollToAnchorPoint(refName) {
      this.restPageActive = !this.restPageActive;
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Back to recommendation page",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      //   const el = document.getElementById(refName).scrollIntoView();
      //   el.scrollIntoView({ behavior: "smooth" });
    },
    getSimilarity(restaurantId) {
      if (this.restaurantJsonRel.length) {
        const dataSimilarity = {
          restaurantId: restaurantId,
          groupId: this.groupId,
        };
        const url = "http://46.18.25.97:8050/similarity";
        axios.post(url, dataSimilarity).then((response) => {
          this.similarityValue = response.data;
        });
      }
    },

    fariness(restId) {
      if (this.restaurantJsonRel.length) {
        if (Object.keys(this.groupInfo).length === 1) {
          return this.attractiveness[Object.keys(this.groupInfo)][restId];
        }
        var groupRelevance = {};
        const userList = Object.keys(this.groupInfo);
        for (const userKey of userList) {
          if (
            Object.keys(this.attractiveness).length != 0 &&
            this.attractiveness[userKey] != undefined
          ) {
            groupRelevance[userKey] = this.attractiveness[userKey][restId];
          }
        }
        var fairList = Object.values(groupRelevance);
        if (fairList.length > 0) {
          if (this.standardDeviation(fairList) > 0) {
            const reverseVariance = 1 - this.standardDeviation(fairList);
            return reverseVariance;
          } else {
            return 0;
          }
        } else {
          return 0;
        }
      }
    },

    standardDeviation(arr) {
      if (this.restaurantJsonRel.length) {
        let mean =
          arr.reduce((acc, curr) => {
            return acc + curr;
          }, 0) / arr.length;

        arr = arr.map((el) => {
          return (el - mean) ** 2;
        });

        let total = arr.reduce((acc, curr) => acc + curr, 0);

        return Math.sqrt(total / arr.length);
      }
    },

    memberDistanceCal(restId) {
      var membersLocation = [];
      var sum = 0;
      var counter = 0;
      var url =
        "http://46.18.25.97:8050/users/location/front/" + String(this.groupId);
      axios.get(url).then((response) => {
        membersLocation = JSON.parse(response.data);
        for (const [key, value] of Object.entries(membersLocation)) {
          this.getDistance(value, restId, key);
        }
      });
    },

    getDistance(p1, restId, key) {
      var url = "http://46.18.25.97:8050/restaurant/" + String(restId);
      var p2 = {
        latitude: -1,
        longitude: -1,
      };
      axios.get(url).then((response) => {
        var rowData = JSON.parse(JSON.stringify(response.data));
        p2 = {
          latitude: rowData.latitude,
          longitude: rowData.longitude,
        };
        var R = 6378137;
        var dLat = this.rad(p2.latitude - p1.latitude);
        var dLong = this.rad(p2.longitude - p1.longitude);
        var a =
          Math.sin(dLat / 2) * Math.sin(dLat / 2) +
          Math.cos(this.rad(p1.latitude)) *
            Math.cos(this.rad(p2.latitude)) *
            Math.sin(dLong / 2) *
            Math.sin(dLong / 2);
        var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        var d = (R * c) / 1000;
        this.membersDistance[key] = parseFloat(d).toFixed(0);
        this.distanceAvr = this.distanceAvr + d;
        this.distanceCounter++;
      });
    },

    rad(x) {
      return (x * Math.PI) / 180;
    },
    checkValidity() {
      this.locationValidity = sessionStorage.getItem("location");
    },

    avrDistance() {
      return parseFloat(
        Object.values(this.membersDistance).reduce((a, b) => a + b, 0) /
          Object.values(this.membersDistance).length
      ).toFixed(0);
    },

    distance(rest) {
      var old_distance = 0;

      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Distance critice added",
      };
      // axios
      //   .get("http://46.18.25.97:8050/group/distance/")
      //   .then(JSON.parse(JSON.stringify(response.data)));
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      var newPreference = {};
      if (rest.price_expensive) {
        newPreference = {
          distance: this.avrDistance() * 1000 - 1,
        };
      } else if (rest.price_mid) {
        newPreference = {
          distance: this.avrDistance() * 1000 - 1,
        };
      } else {
        newPreference = {
          distance: this.avrDistance() * 1000 - 1,
        };
      }
      const distance_url =
        "http://46.18.25.97:8050/group/distance/" + String(this.groupId);
      axios.get(distance_url).then((response) => {
        old_distance = JSON.parse(JSON.stringify(response.data));
        var url =
          "http://46.18.25.97:8050/preferences/group/distance/" +
          String(this.groupId);
        axios.post(url, newPreference).then(() => {
          url =
            "http://46.18.25.97:8050/recommendations/relevance/" +
            String(this.groupId);
          axios.get(url).then((response) => {
            this.restaurantJsonRel = JSON.parse(JSON.stringify(response.data));

            var url =
              "http://46.18.25.97:8050/recommendations/popularity/" +
              String(this.groupId);
            axios.get(url).then((response) => {
              this.restaurantJson = JSON.parse(JSON.stringify(response.data));
              console.log(
                this.restaurantJsonRel.length + this.restaurantJson.length
              );
              if (
                this.restaurantJsonRel.length + this.restaurantJson.length <
                1
              ) {
                this.$q.notify({
                  message: "There is no restaurant closer than this.",
                  icon: "announcement",
                  color: "red",
                });
                var interactionData = {
                  group_id: this.group_id_intract,
                  interaction: "Distance critice added",
                };
                const distance_url =
                  "http://46.18.25.97:8050/group/distance/" +
                  String(this.groupId);
                axios
                  .get(distance_url)
                  .then(JSON.parse(JSON.stringify(response.data)));
                axios
                  .post("http://46.18.25.97:8050/interaction", interactionData)
                  .then();
                var newPreference = {};
                if (rest.price_expensive) {
                  newPreference = {
                    distance: old_distance,
                  };
                } else if (rest.price_mid) {
                  newPreference = {
                    distance: old_distance,
                  };
                } else {
                  newPreference = {
                    distance: old_distance,
                  };
                }
                var url =
                  "http://46.18.25.97:8050/preferences/group/distance/" +
                  String(this.groupId);
                axios.post(url, newPreference).then(() => {
                  url =
                    "http://46.18.25.97:8050/recommendations/relevance/" +
                    String(this.groupId);
                  axios.get(url).then((response) => {
                    this.restaurantJsonRel = JSON.parse(
                      JSON.stringify(response.data)
                    );
                  });
                  var url =
                    "http://46.18.25.97:8050/recommendations/popularity/" +
                    String(this.groupId);
                  axios.get(url).then((response) => {
                    this.restaurantJson = JSON.parse(
                      JSON.stringify(response.data)
                    );
                  });
                });
              } else {
                this.restPageActive = !this.restPageActive;
              }
            });
          });
        });
      });
    },

    price(range) {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Pice " + String(range) + "added",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      var newPreference = {};
      if (range === "eco") {
        newPreference = {
          price_eco: true,
          price_mid: false,
          price_expensive: false,
        };
      } else if (range === "mid") {
        newPreference = {
          price_eco: false,
          price_mid: true,
          price_expensive: false,
        };
      } else {
        newPreference = {
          price_eco: false,
          price_mid: false,
          price_expensive: true,
        };
      }
      const headers = {
        "Content-Type": "application/json",
      };
      var url =
        "http://46.18.25.97:8050/preferences/group/price/" +
        String(this.groupId);
      axios
        .post(url, newPreference, {
          headers: headers,
        })
        .then(() => {
          url =
            "http://46.18.25.97:8050/recommendations/relevance/" +
            String(this.groupId);
          axios.get(url).then((response) => {
            this.restaurantJsonRel = JSON.parse(JSON.stringify(response.data));
          });
          var url =
            "http://46.18.25.97:8050/recommendations/popularity/" +
            String(this.groupId);
          axios.get(url).then((response) => {
            this.restaurantJson = JSON.parse(JSON.stringify(response.data));
          });
          this.restPageActive = !this.restPageActive;
        });
    },
  },
  mounted() {
    if (String(sessionStorage.getItem("Selected")) === "true") {
      this.endOfSession = true;
    } else {
      this.endOfSession = false;
    }
    var grouIdTested = sessionStorage.getItem("group_id");
    var url =
      "http://46.18.25.97:8050/recommendations/popularity/" +
      String(grouIdTested);
    axios.get(url).then((response) => {
      this.restaurantJson = JSON.parse(JSON.stringify(response.data));
      for (var resturant of Object.values(this.restaurantJson)) {
        this.model3[JSON.parse(resturant).id] = ref(0);
      }
      var url = "http://46.18.25.97:8050/bookmarked/" + String(grouIdTested);
      axios.get(url).then((response) => {
        for (var bookedrest of response.data) {
          this.bookmarked.push(bookedrest);
        }
        for (var resturant of Object.values(this.restaurantJson)) {
          if (typeof response.data !== "undefined") {
            if (
              Object.values(response.data).includes(JSON.parse(resturant).id)
            ) {
              this.model3[JSON.parse(resturant).id] = ref(1);
            } else {
              this.model3[JSON.parse(resturant).id] = ref(0);
            }
          } else {
            this.model3[JSON.parse(resturant).id] = ref(0);
          }
        }
        this.pageload = true;
      });
    });
    url = "http://46.18.25.97:8050/recommendations/relevance/" + grouIdTested;
    axios.get(url).then((response) => {
      this.restaurantJsonRel = JSON.parse(JSON.stringify(response.data));
    });
    const urlAttract =
      "http://46.18.25.97:8050/recommendations/attractiveness/" + grouIdTested;
    axios.get(urlAttract).then((response) => {
      this.attractiveness = JSON.parse(JSON.stringify(response.data));
    });
  },
};
</script>

<style>
.footer {
  position: fixed;
  bottom: 0;
  width: 100%;
}
.popActive {
  background: rgb(218, 218, 232);
}
.relActive {
  background: rgb(218, 218, 232);
}
.no-tasks {
  opacity: 0.7;
}
.icon {
  opacity: 0.2;
}
.clear {
  padding-bottom: 80px;
}
.scroll {
  margin-bottom: 70px;
}
.button-back {
  margin-top: 5px;
  margin-left: 5px;
}
.centering {
  border-radius: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
}
.card-position {
  padding-top: 0px;
}
.parent {
  display: flex;
  justify-content: center;
  align-items: center;
}
.critique-btn {
  margin: 1px auto;
}
</style>
