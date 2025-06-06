<template>
  <div class="q-pa-md q-gutter-sm" v-if="selectToggle">
    <q-dialog v-model="confirm" persistent>
      <q-card>
        <q-card-section class="row items-center" align="left">
          <span class="q-ml-sm"
            >Do you want to select this restaurant as your final choice?</span
          >
        </q-card-section>

        <q-card-actions align="left">
          <q-btn
            flat
            label="CANCEL"
            color="primary"
            v-close-popup
            @click="selectToggleFunc()"
          />
          <q-btn
            flat
            label="SELECT"
            color="green"
            v-close-popup
            @click="
              select(
                bookedRestId,
                fariness(bookedRestId),
                attractiveness,
                getSimilarity(bookedRestId)
              )
            "
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  <div v-if="bookmarked.length !== 0">
    <div v-if="endOfSession">
      <div class="q-pa-md" style="max-width: 400px">
        <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
          <div class="q-pa-md row items-start q-gutter-md">
            <q-card class="my-card" style="width: 100%">
              <q-card-section style="width: 100%">
                <p style="font-weight: bold">
                  Thank you for participating in our user study. For evaluating
                  our system, please answer to the following questions.
                </p>
                <q-separator />
                <p class="question">
                  1. I think that I would like to use this system frequently.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel1"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  2. I found the system unnecessarily complex.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel2"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">3. I tought the system was easy to use.</p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel3"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  4. I think that I would need the support of a technical person
                  to be able to use this system.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel4"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  5. I found the various functions in the system were well
                  integrated.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel5"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  6. I tought there was too much inconsistency in this system.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel6"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  7. I would imagine that most people would learn to use this
                  system very quickly.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel7"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  8. I found the system very cumbersome to user.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel8"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  9. I felt very confident using the system.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel9"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
                <p class="question">
                  10. I needed to learn a lot of things before I could get going
                  with this system.
                </p>
                <div class="parent">
                  <div class="q-pa-md">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="ratingModel10"
                        size="2.5em"
                        color="yellow-8"
                        icon="star_border"
                        icon-selected="star"
                      />
                    </div>
                  </div>
                </div>
                <q-separator />
              </q-card-section>
            </q-card>
          </div>
          <div class="parent">
            <q-btn label="Submit" type="submit" color="primary" />
            <q-btn label="Reset" type="reset" color="grey" flat />
          </div>
        </q-form>
      </div>
    </div>
    <div v-else>
      <div v-if="pageload && prestListValidity">
        <div v-if="restPageActive">
          <q-btn
            round
            color="primary"
            icon="chevron_left"
            position="top-left"
            @click="backToBookmark()"
            size="0.7em"
            class="button-back"
          />
          <div
            v-for="bookedId in navigated"
            :key="bookedId"
            style="width: 100%"
          >
            <div
              class="card-position q-pa-md row items-start q-gutter-md"
              style="margin: auto; width: 100%"
            >
              <q-card class="my-card" style="width: 90%; margin: auto">
                <q-card-section style="padding: 5px">
                  <div class="text-h6 q-mb-xs">
                    {{ restuaurants[bookedId]["name"] }}
                  </div>
                  <div class="q-pa-md" style="padding: 5px">
                    <div class="q-gutter-y-md column" style="width: 30px">
                      <q-rating
                        v-model="model3"
                        max="1"
                        size="30px"
                        color="red"
                        color-selected="red-9"
                        icon="favorite_border"
                        icon-selected="favorite"
                        @click="submitRemoveBookmark(bookedId)"
                      />
                    </div>
                  </div>
                </q-card-section>
                <img
                  :src="getLogo(restuaurants[bookedId].logo)"
                  style="height: 200px; padding: 2px; border-radius: 5px"
                />
                <q-card-section class="q-pt-none">
                  <div class="q-pa-md row items-start q-gutter-md">
                    <q-card class="my-card">
                      <q-card-section>
                        <p>
                          Address: {{ restuaurants[bookedId]["address"] }},
                          {{ restuaurants[bookedId]["city"] }}, Italy
                        </p>
                        <p>
                          <a
                            :href="links[restuaurants[bookedId].name]"
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
                          {{ JSON.parse(bookedId).id }}
                          Popularity:
                          {{ popularity(bookedId) }}
                          <q-linear-progress
                            :value="popularityObj[bookedId]"
                            color="red"
                            class="q-mt-sm"
                          />
                        </p>
                        <p>
                          Selected as the final choice:
                          {{ selectedPopularity(bookedId) }}
                          <q-linear-progress
                            :value="selectedPopularityObj[bookedId]"
                            class="q-mt-sm"
                          />
                        </p>
                        <div
                          v-for="(
                            userAttractiveness, name, index
                          ) in attractiveness"
                          :key="index"
                        >
                          <p>
                            Attractivemess for you:
                            <q-linear-progress
                              :value="userAttractiveness[bookedId]"
                              :color="groupInfo[name][0]"
                              class="q-mt-sm"
                            />
                          </p>
                        </div>
                        <div style="width: 100%">
                          {{ getSimilarity(bookedId) }}
                          Popularity in people like yours:
                          <q-linear-progress
                            :value="similarityValue[bookedId]"
                            color="orange"
                            class="q-mt-sm"
                          />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>

                  <div class="q-pa-md row items-start q-gutter-md">
                    <q-card class="my-card" style="width: 100%">
                      <q-card-section style="width: 100%">
                        <p v-show="Boolean(restuaurants[bookedId].price_eco)">
                          Price: Economic
                        </p>
                        <div
                          class="parent"
                          v-show="Boolean(restuaurants[bookedId].price_eco)"
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
                        <p v-show="Boolean(restuaurants[bookedId].price_mid)">
                          Price: Mid-range
                        </p>
                        <div
                          class="parent"
                          v-show="Boolean(restuaurants[bookedId].price_mid)"
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
                        <p
                          v-show="
                            Boolean(restuaurants[bookedId].price_expensive)
                          "
                        >
                          Price: Expensive
                        </p>
                        <div
                          class="parent"
                          v-show="
                            Boolean(restuaurants[bookedId].price_expensive)
                          "
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
                          <q-btn
                            color="grey"
                            label="$$$"
                            class="critique-btn"
                          />
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
                        {{ memberDistanceCal(bookedId) }}
                        <div v-for="(value, key) in groupInfo" :key="key">
                          {{ value[1] }}'s distance
                          {{ membersDistance[key] }} KM
                        </div>
                        <p></p>
                        Group's average distance
                        {{ avrDistance(restuaurants[bookedId]) }} KM
                        <p></p>
                        <div class="parent">
                          <q-btn
                            color="primary"
                            label="Closer"
                            @click="distance(restuaurants[bookedId])"
                          />
                        </div>
                      </q-card-section>
                    </q-card>
                  </div>
                </q-card-section>
                <q-card-section style="padding-top: 0px">
                  <div
                    class="q-pa-md"
                    style="max-width: 350px; padding-top: 0px"
                  >
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
                              category + ' (' + String(foodList.length) + ')'
                            "
                          >
                            <div class="q-pa-md" style="max-width: 350px">
                              <div
                                v-for="(food, indexIn) in foodList"
                                :key="indexIn"
                              >
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
                <div class="parent">
                  <q-card-section>
                    <q-btn
                      color="primary"
                      label="Select"
                      @click="selectToggleFunc(bookedId)"
                      class="critique-btn"
                    />
                  </q-card-section>
                </div>
              </q-card>
            </div>
          </div>
        </div>
        <div v-else>
          <div
            v-for="bookedId in bookmarked"
            :key="bookedId"
            style="float: left; width: 48%; padding: 0px; margine: 1px"
          >
            <div
              class="q-pa-md row items-start q-gutter-md"
              style="width: 100%; padding: 0px; margin: 1px auto"
              @click="navigateToRestPage(bookedId)"
            >
              <q-card class="my-card">
                <img
                  :src="getLogo(restuaurants[bookedId].logo)"
                  style="height: 200px; padding: 2px; border-radius: 5px"
                />

                <q-card-section style="padding: 0px">
                  <p style="margin: 5px">
                    <strong>{{ restuaurants[bookedId].name }}</strong>
                  </p>
                  <p
                    v-if="
                      suggestionEvaluation(
                        fariness(bookedId),
                        attractiveness,
                        bookedId
                      ) >= maxSuggestion
                    "
                    style="margin: 5px; color: green"
                  >
                    This our suggestion for you
                  </p>
                </q-card-section>
                <div
                  class="q-pa-md row items-start q-gutter-md"
                  style="padding: 0px margin: 1px"
                >
                  <div style="width: 100%">
                    {{ JSON.parse(bookedId).id }}
                    Popularity:
                    {{ popularity(bookedId) }}
                    <q-linear-progress
                      :value="popularityObj[bookedId]"
                      color="red"
                      class="q-mt-sm"
                    />
                  </div>
                  <div style="width: 100%">
                    Selected as the final choice:
                    {{ selectedPopularity(bookedId) }}
                    <q-linear-progress
                      :value="selectedPopularityObj[bookedId]"
                      class="q-mt-sm"
                    />
                  </div>
                </div>
                <div v-if="restaurantJsonRel.length">
                  <div
                    class="q-pa-md row items-start q-gutter-md"
                    style="padding: 0px margin: 1px"
                  >
                    <div
                      v-for="(
                        userAttractiveness, name, index
                      ) in attractiveness"
                      :key="index"
                      style="width: 100%"
                    >
                      <p>
                        Attractivemess for you:
                        <q-linear-progress
                          :value="userAttractiveness[bookedId]"
                          :color="groupInfo[name][0]"
                          class="q-mt-sm"
                        />
                      </p>
                    </div>
                    <div style="width: 100%">
                      {{ getSimilarity(bookedId) }}
                      Popularity in people like yours:
                      <q-linear-progress
                        :value="similarityValue[bookedId]"
                        color="orange"
                        class="q-mt-sm"
                      />
                    </div>
                  </div>
                </div>
                <div
                  class="q-pa-md row items-start q-gutter-md"
                  style="padding: 0px; margin: 1px auto"
                >
                  <p v-if="Boolean(restuaurants[bookedId]['price_eco'])">
                    Price: Economic
                  </p>

                  <p v-if="Boolean(restuaurants[bookedId]['price_mid'])">
                    Price: Mid-range
                  </p>

                  <p v-if="Boolean(restuaurants[bookedId]['price_expensive'])">
                    Price: Expensive
                  </p>
                  <br />
                  {{ checkValidity() }}
                  <div v-if="String(locationValidity) === 'true'">
                    {{ memberDistanceCal(bookedId) }}
                    <div v-for="(value, key) in groupInfo" :key="key">
                      {{ value[1] }}'s distance {{ membersDistance[key] }} KM
                    </div>
                    <p></p>
                    <!-- Group's average distance
                    {{ avrDistance(restuaurants[bookedId]) }} KM -->
                  </div>
                </div>
                <div class="parent">
                  <q-card-section>
                    <q-btn
                      color="primary"
                      label="Select"
                      @click="selectToggleFunc(bookedId)"
                      class="critique-btn"
                    />
                  </q-card-section>
                </div>
              </q-card>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <div class="no-tasks absolute-center text-h5 text-primary text-center">
      You have not bookmarked any restaurant
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
export default {
  props: ["groupInfo", "groupId"],
  emits: ["critiqueIssued"],
  data() {
    return {
      selectedPopularityObj: {},
      popularityObj: {},
      endOfSession: false,
      selectToggle: false,
      maxSuggestion: 0,
      links: require(`../assets/external_link.json`),
      prestListValidity: false,
      navigated: [],
      restPageActive: false,
      restPageList: [],
      membersDistance: {},
      bookmarked: [],
      pageload: false,
      restuaurants: {},
      attractiveness: {},
      restaurantJsonRel: {},
      similarityValue: {},
      model3: ref(1),
      locationValidity: false,
      menuList: {},
      confirm: "",
      suggestionObj: {},
      bookedRestId: -1,
      similarityObj: {},
      group_id_intract: this.groupId,
      ratingModel1: ref(0),
      ratingModel2: ref(0),
      ratingModel3: ref(0),
      ratingModel4: ref(0),
      ratingModel5: ref(0),
      ratingModel6: ref(0),
      ratingModel7: ref(0),
      ratingModel8: ref(0),
      ratingModel9: ref(0),
      ratingModel10: ref(0),
    };
  },
  methods: {
    onSubmit() {
      var flag1 = true;
      var flag2 = true;
      var flag3 = true;
      var flag4 = true;
      var flag5 = true;
      var flag6 = true;
      var flag7 = true;
      var flag8 = true;
      var flag9 = true;
      var flag10 = true;
      if (this.ratingModel1 < 1) {
        flag1 = false;
        this.$q.notify({
          message: "Please answer the question 1.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel2 < 1) {
        flag2 = false;
        this.$q.notify({
          message: "Please answer the question 2.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel3 < 1) {
        flag3 = false;
        this.$q.notify({
          message: "Please answer the question 3.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel4 < 1) {
        flag4 = false;
        this.$q.notify({
          message: "Please answer the question 4.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel5 < 1) {
        flag5 = false;
        this.$q.notify({
          message: "Please answer the question 5.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel6 < 1) {
        flag6 = false;
        this.$q.notify({
          message: "Please answer the question 6.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel7 < 1) {
        flag7 = false;
        this.$q.notify({
          message: "Please answer the question 7.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel8 < 1) {
        flag8 = false;
        this.$q.notify({
          message: "Please answer the question 8.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel9 < 1) {
        flag9 = false;
        this.$q.notify({
          message: "Please answer the question 9.",
          icon: "announcement",
          color: "red",
        });
      }
      if (this.ratingModel10 < 1) {
        flag10 = false;
        this.$q.notify({
          message: "Please answer the question 10.",
          icon: "announcement",
          color: "red",
        });
      }
      if (
        (flag1 === true) &
        (flag2 === true) &
        (flag3 === true) &
        (flag4 === true) &
        (flag5 === true) &
        (flag6 === true) &
        (flag7 === true) &
        (flag8 === true) &
        (flag9 === true) &
        (flag10 === true)
      ) {
        var susData = {
          group_id: parseInt(this.group_id_intract),
          q1: this.ratingModel1,
          q2: this.ratingModel2,
          q3: this.ratingModel3,
          q4: this.ratingModel4,
          q5: this.ratingModel5,
          q6: this.ratingModel6,
          q7: this.ratingModel7,
          q8: this.ratingModel8,
          q9: this.ratingModel9,
          q10: this.ratingModel10,
        };
        axios.post("http://46.18.25.97:8050/sus", susData).then();
        sessionStorage.removeItem("group_id");
        sessionStorage.removeItem("location");
        sessionStorage.removeItem("group_members_status");
        sessionStorage.removeItem("Selected");
        sessionStorage.clear();

        this.$q.notify({
          message: "Your answers have been saved.",
          icon: "announcement",
          color: "primary",
        });
        setTimeout(function () {
          location.reload();
        }, 3000);
      }
    },
    onReset() {
      sessionStorage.removeItem("group_id");
      sessionStorage.removeItem("location");
      sessionStorage.removeItem("group_members_status");
      sessionStorage.removeItem("Selected");
      sessionStorage.clear();
      location.reload();
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
    selectToggleFunc(bookedId) {
      this.bookedRestId = bookedId;
      this.selectToggle = !this.selectToggle;
    },
    select(bookedId, fair, attr, sim) {
      var selectedData = {
        group_id: parseInt(this.group_id_intract),
        restaurant_id: parseInt(bookedId),
      };
      axios.post("http://46.18.25.97:8050/selected", selectedData).then();
      var interactionData = {
        group_id: this.group_id_intract,
        interaction:
          "Restaurant " + String(bookedId) + " selected as final choice",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      var strToWrite = "";
      strToWrite += "GROUPID, \t" + String(this.groupId) + "\n";
      for (var userId of Object.keys(this.groupInfo)) {
        strToWrite += "USERID, \t" + String(userId) + "\n";
        strToWrite += "Name, \t" + String(this.groupInfo[userId][1]) + "\n";
      }
      strToWrite += "SELECTED RESTAURANT, \t" + String(bookedId) + "\n";
      strToWrite += "SELECTED FAIRNESS, \t" + String(fair) + "\n";
      strToWrite +=
        "SELECTED SUGGESTION SCORE, \t" +
        String(this.suggestionObj[bookedId]) +
        "\n";
      if (attr.length > 0) {
        for (var userId of Object.keys(this.groupInfo)) {
          strToWrite +=
            "SELECTED USER " +
            String(userId) +
            " ATTRACTIVENESS, \t" +
            "\t" +
            String(attr[userId][bookedId]) +
            "\n";
        }
      }
      strToWrite +=
        "SELECTED SIMILARITY, \t" + String(this.similarityObj[bookedId]) + "\n";
      for (var bookedResId of this.bookmarked) {
        strToWrite += "RESTAURANT, \t" + String(bookedResId) + "\n";
        strToWrite +=
          "FAIRNESS, \t" + String(this.fariness(bookedResId)) + "\n";
        strToWrite +=
          "SELECTED SUGGESTION SCORE, \t" +
          String(this.suggestionObj[bookedResId]) +
          "\n";
        if (attr.length > 0) {
          for (var userId of Object.keys(this.groupInfo)) {
            strToWrite +=
              "USER " +
              String(userId) +
              " ATTRACTIVENESS, \t" +
              "\t" +
              String(attr[userId][bookedResId]) +
              "\n";
          }
        }
        strToWrite +=
          "SIMILARITY, \t" + String(this.similarityObj[bookedResId]) + "\n";
      }
      var resultData = {
        groupId: this.groupId,
        description: strToWrite,
      };
      const url = "http://46.18.25.97:8050/group/result";
      axios.post(url, resultData).then((response) => {
        sessionStorage.setItem("Selected", true);
        this.endOfSession = true;
      });
    },
    suggestionEvaluation(fair, attract, idRest) {
      var attractSum = 0;
      for (var restAttract of Object.values(attract)) {
        attractSum = attractSum + restAttract[idRest];
      }
      var attrAvr = attractSum / Object.keys(attract).length;
      if (attrAvr + fair > this.maxSuggestion) {
        this.maxSuggestion = attrAvr + fair;
      }
      this.suggestionObj[idRest] = attrAvr + fair;
      return attrAvr + fair;
    },
    getLogo(logo) {
      return require(`../assets/logo/` + String(logo));
    },
    backToBookmark() {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Back to bookmark page",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.restPageActive = false;
    },
    getSimilarity(restaurantId) {
      if (this.restaurantJsonRel.length) {
        const dataSimilarity = {
          restaurantId: restaurantId,
          groupId: this.groupId,
        };
        const url = "http://46.18.25.97:8050/similarity";
        axios.post(url, dataSimilarity).then((response) => {
          this.similarityValue[restaurantId] = response.data;
          this.similarityObj[restaurantId] = response.data;
          return response.data;
        });
      } else {
        this.similarityValue[restaurantId] = 0;
        return 0;
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
      } else {
        return 0;
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
      } else {
        return 0;
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
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Distance critice added",
      };
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
      var url =
        "http://46.18.25.97:8050/preferences/group/distance/" +
        String(this.groupId);
      axios.post(url, newPreference).then(() => {
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
        this.restPageActive = !restPageActive;
      });
    },

    price(range) {
      this.$emit("critiqueIssued");
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
    submitRemoveBookmark(restaurantId) {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Restaurant " + String(restaurantId) + " Unbooked",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      var bookmarkObj = {
        restaurant_id: restaurantId,
        group_id: sessionStorage.getItem("group_id"),
      };
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
    },
    navigateToRestPage(restid) {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Vist Restaurant " + String(restid) + " page",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.navigated = [];
      this.navigated.push(restid);
      this.restPageActive = true;
      const urlmnue = "http://46.18.25.97:8050/restaurant/menu/" + restid;
      axios.get(urlmnue).then((response) => {
        this.menuList = JSON.parse(JSON.stringify(response.data));
      });
    },
  },
  mounted() {
    if (String(sessionStorage.getItem("Selected")) === "true") {
      this.endOfSession = true;
    } else {
      this.endOfSession = false;
    }
    this.prestListValidity = false;
    var url = "http://46.18.25.97:8050/bookmarked/" + String(this.groupId);
    axios.get(url).then((response) => {
      for (var bookedrest of response.data) {
        this.bookmarked.push(bookedrest);
        var urlRest =
          "http://46.18.25.97:8050/restaurant/" + String(bookedrest);
        axios.get(urlRest).then((response) => {
          this.restuaurants[response.data.id] = response.data;
        });
        const urlAttract =
          "http://46.18.25.97:8050/recommendations/attractiveness/" +
          this.groupId;
        axios.get(urlAttract).then((response) => {
          this.attractiveness = JSON.parse(JSON.stringify(response.data));
        });
      }
      url = "http://46.18.25.97:8050/recommendations/relevance/" + this.groupId;
      axios.get(url).then((response) => {
        this.restaurantJsonRel = JSON.parse(JSON.stringify(response.data));
        this.pageload = true;
      });
      this.prestListValidity = true;
    });
  },
};
</script>

<style lang="sass" scoped>
.my-card
  width: 100%
</style>
