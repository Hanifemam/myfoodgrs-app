<template>
  <div
    class="q-pa-md"
    style="padding-bottom: 70px; padding-top: 0px; margin-top: 0px"
  >
    <div v-if="!signed">
      <div class="parent">
        <q-btn-toggle
          v-model="signPage"
          push
          toggle-color="primary"
          :options="[
            { label: 'Sign up', value: 'up' },
            { label: 'Log in', value: 'in' },
          ]"
          style="margin-bottom: 20px"
        />
      </div>
      <div v-if="signPage === 'up'">
        <q-form
          @submit="onSubmit('up')"
          @reset="onReset('up')"
          class="q-gutter-md"
        >
          <q-input
            filled
            v-model="name"
            label="Name *"
            hint="Insert your name"
            :rules="[
              (val) => (val && val.length > 0) || 'Please type something',
              (val) => !!val || 'Field is required',
            ]"
            class="required"
          />

          <q-input
            filled
            v-model="email"
            label="User name"
            :rules="[(val) => !!val || 'Field is required']"
            class="required"
          />
          <q-input
            filled
            type="password"
            v-model="password"
            label="Password *"
            :rules="[(val) => !!val || 'Field is required']"
            class="required"
          />
          <div
            class="q-pa-md row items-start q-gutter-md parent"
            style="margin: 0 auto; padding-right: 0px"
          >
            <q-card
              class="my-card parent"
              style="width: 100%; margin: 0px auto; opacity: 0.9"
            >
              <q-card-section style="padding: 10px; text-align: justify">
                Thanks for participating in this user study. This study aims to
                evaluate the quality of the provided supporting functionalities
                in supporting the organizer of an event in finding proper
                restaurant for her/his group. We are collecting your data: Name,
                Email, Age, Nationality, and Food Preferences. By clicking on
                the button below you give us the permission to use your data in
                our study and analysis.
              </q-card-section>
            </q-card>
          </div>
          <div class="parent">
            <q-toggle v-model="accept" label="I accept the license and terms" />
          </div>
          <div class="parent">
            <q-btn label="Submit" type="submit" color="primary" />
            <!-- <q-btn
              label="Reset"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
            /> -->
          </div>
        </q-form>
      </div>
      <div v-else>
        <q-form
          @submit="onSubmit('in')"
          @reset="onReset('in')"
          class="q-gutter-md"
        >
          <q-input
            filled
            v-model="email"
            label="User name"
            :rules="[(val) => !!val || 'Field is required']"
            class="required"
          />
          <q-input
            filled
            type="password"
            v-model="password"
            label="Password *"
            :rules="[(val) => !!val || 'Field is required']"
            class="required"
          />

          <div>
            <div class="parent">
              <q-btn label="Submit" type="submit" color="primary" />
              <q-btn
                label="Reset"
                type="reset"
                color="primary"
                flat
                class="q-ml-sm"
              />
            </div>
          </div>
        </q-form>
      </div>
    </div>
    <div v-else>
      <div
        class="q-pa-md row items-start q-gutter-md parent"
        style="margin: 0 auto; padding-right: 0px; padding-left: 0px"
      >
        <q-card
          class="my-card parent"
          style="width: 100%; margin: 0px auto; opacity: 0.9"
        >
          <q-item style="width: 100%">
            <q-item-section avatar>
              <q-avatar>
                <q-icon name="person" color="primary" />
              </q-avatar>
            </q-item-section>

            <q-item-section>
              <q-item-label>Welcome {{ submittedName }} </q-item-label>
              <q-item-label caption
                >Lets find a restaurant for your group</q-item-label
              >
            </q-item-section>
          </q-item>
        </q-card>
      </div>
      <div class="q-pa-md" style="width: 100%; padding: 0px 0px 0px 0px">
        <q-stepper
          v-model="step"
          ref="stepper"
          contracted
          color="primary"
          animated
        >
          <q-step
            :name="1"
            title="Account created"
            icon="account_circle"
            :done="step > 1"
          >
            You have created your account and rated some restaurant. The next
            step is constructing you group and finding a proper restaurant for
            all group members. Please wait until we have enough number of users
            to create a group for you.
          </q-step>

          <q-step
            :name="2"
            title="Group Created"
            icon="groups"
            :done="step > 2"
          >
            Your group has been created. Please use the application to find
            proper restaurant for your group.
          </q-step>

          <q-step
            :name="3"
            title="Restaurant selected"
            icon="check_circle_outline"
            :done="step > 3"
          >
            {{ postRatingMassegeWaitning }}
          </q-step>
          <q-step
            :name="4"
            title="Restaurant selected"
            icon="check_circle_outline"
            :done="step === 4"
          >
            You are done. Thanks for participating in this study.
          </q-step>
        </q-stepper>
      </div>
      <div v-if="!infoValidation">
        <div
          style="
            margin: 8px 0px;
            padding-right: 0px;
            padding-left: 0px;
            padding-top: 0px;
          "
        >
          <q-card
            class="my-card parent"
            style="width: 100%; margin: 0px auto; opacity: 0.9"
          >
            <div class="q-pa-md" style="width: 90%">
              <q-form
                @submit="onSubmitUserInfo"
                @reset="onResetUserInfo"
                class="q-gutter-md"
              >
                <div class="q-pa-md" style="margin-top: 0px">
                  <div class="q-gutter-md">
                    <q-select
                      v-model="genderModel"
                      :options="genderOption"
                      label="Gender"
                      style="
                        padding-right: 0px;
                        padding-left: 0px;
                        padding-top: 0px;
                        margin-top: 0px;
                      "
                    />
                  </div>
                </div>

                <div class="q-pa-md" style="margin-top: 0px">
                  <div class="q-gutter-md">
                    <q-select
                      v-model="ageModel"
                      :options="ageOption"
                      label="Age"
                      style="
                        padding-right: 0px;
                        padding-left: 0px;
                        padding-top: 0px;
                        margin-top: 0px;
                      "
                    />
                  </div>
                </div>

                <div class="q-pa-md" style="margin-top: 0px">
                  <div class="q-gutter-md">
                    <q-select
                      v-model="countryModel"
                      :options="countryOption"
                      label="Nationality"
                      style="
                        padding-right: 0px;
                        padding-left: 0px;
                        padding-top: 0px;
                        margin-top: 0px;
                      "
                    />
                  </div>
                </div>
                <div class="q-gutter-sm">
                  <p>
                    Please select at most two types of dish that you prefer to
                    eat in the event:
                  </p>
                  <div>
                    <q-checkbox
                      v-model="PASTAModel"
                      :label="food_name_change('PASTA')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="CARNEModel"
                      :label="food_name_change('CARNE')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="PESCEModel"
                      :label="food_name_change('PESCE')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="RISOModel"
                      :label="food_name_change('RISO')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="CROSTACEI_E_MOLLUSCHIModel"
                      :label="food_name_change('CROSTACEI_E_MOLLUSCHI')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="PIZZAModel"
                      :label="food_name_change('PIZZA')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="VERDUREModel"
                      :label="food_name_change('VERDURE')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="GNOCCHIModel"
                      :label="food_name_change('GNOCCHI')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="TORTELLINIModel"
                      :label="food_name_change('TORTELLINI')"
                      style="margin: 0px 16px 0px 0px"
                    />
                    <q-checkbox
                      v-model="LEGUMIModel"
                      :label="food_name_change('LEGUMI')"
                      style="margin: 0px 16px 0px 0px"
                    />
                  </div>
                </div>
                <div class="q-gutter-sm">
                  <p>Please select the types of dish that you like:</p>
                  <div>
                    <q-checkbox
                      v-model="french"
                      label="French"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="chinese"
                      label="Chinese"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="jpan"
                      label="Japanese"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="italian"
                      label="Italian"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="greek"
                      label="Greek"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="indian"
                      label="Indian"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="spain"
                      label="Spanish"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="lebanan"
                      label="Lebanese"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="moroccan"
                      label="Moroccan"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="turkish"
                      label="Turkish"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                    <q-checkbox
                      v-model="thai"
                      label="Thai"
                      color="primary"
                      style="margin-left: 0px; margin-right: 26px"
                    />
                  </div>
                </div>
                <div class="parent">
                  <q-btn label="Submit" type="submit" color="primary" />
                  <!-- <q-btn
                    label="Reset"
                    type="reset"
                    color="primary"
                    flat
                    class="q-ml-sm"
                  /> -->
                </div>
              </q-form>
            </div>
          </q-card>
        </div>
      </div>
      <div v-if="infoValidation && !ratingValidation">
        <!-- <div
          class="q-pa-md row items-start q-gutter-md parent"
          style="
            margin: 0 auto;
            padding-right: 0px;
            padding-left: 0px;
            padding-top: 0px;
          "
        > -->
        <!-- <q-card
          class="my-card"
          style="width: 100%; margin: 0px auto; opacity: 0.9"
        > -->
        <q-card class="my-card" style="width: 100%; margin: 8px 0px">
          <q-card-section>
            <span>
              Rate following restaurants based on your
              <span style="font-weight: bold">PERSONAL PREFERENCE</span>
              .
            </span>
          </q-card-section>
        </q-card>
        <div style="margin: 8px 0px">
          <q-card class="my-card" style="width: 100%; margin: auto">
            <q-card-section>
              Progress in rating:
              <q-linear-progress
                size="10px"
                :value="progress"
                class="q-mt-md"
              />
            </q-card-section>
          </q-card>
        </div>

        <div v-for="(rest, index) in nextRest" :key="index">
          <div v-if="(step < 3 && index < 10) || step >= 3">
            <q-card class="my-card" style="width: 100%; margin: auto">
              <q-card-section>
                <q-img
                  :src="getLogo(rest.logo)"
                  style="height: 200px; padding: 2px; border-radius: 5px"
                />
                <q-card-section style="padding: 5px">
                  <q-rating
                    v-model="ratingModel"
                    size="2em"
                    color="yellow-8"
                    icon="star_border"
                    icon-selected="star"
                  />
                  <p style="font-weight: bold; margin-bottom: 1px">
                    {{ rest.name }}
                  </p>
                  <p style="margin-bottom: 1px">Address: {{ rest.address }}</p>
                  <p style="padding-bottom: 2px; margin-bottom: 0px">
                    <a
                      :href="links[rest.name]"
                      style="text-decoration: none"
                      target="_blank"
                      ><b>Link</b></a
                    >
                  </p>
                  <q-list class="rounded-borders">
                    <q-expansion-item
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
                          :label="
                            food_name_change(category) +
                            ' (' +
                            String(foodList.length) +
                            ')'
                          "
                        >
                          <div class="q-pa-md" style="width: 100%">
                            <div
                              v-for="(food, indexIn) in foodList"
                              :key="indexIn"
                            >
                              <q-list>
                                <q-item clickable v-ripple>
                                  <q-item-section>{{ food }}</q-item-section>
                                </q-item>
                              </q-list>
                              <q-separator />
                            </div>
                          </div>
                        </q-expansion-item>
                      </div>
                    </q-expansion-item>
                  </q-list>
                </q-card-section>
                <div class="parent">
                  <q-btn
                    label="Submit and Next"
                    type="submit"
                    @click="rated(rest.id)"
                    color="primary"
                  />
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
        <div class="centering"></div>
        <!-- </q-card> -->
        <!-- </div> -->
      </div>
      <div
        v-if="infoValidation && ratingValidation && itemSelectedHere"
        style="margin: 8px 0px"
      >
        <div
          v-if="step < 4 && Object.keys(nextRest).length > 0"
          style="margin: 0px 0px 8px 0px; padding-left: 0px; padding-right: 0px"
        >
          <q-card class="my-card" style="width: 100%; margin: 8px 0px">
            <q-card-section>
              <p v-html="postRatingMassege"></p>
            </q-card-section>
          </q-card>
          <q-card class="my-card" style="width: 100%; margin: auto">
            <q-card-section>
              Progress in rating:
              <q-linear-progress
                size="10px"
                :value="progressPost"
                class="q-mt-md"
              />
            </q-card-section>
          </q-card>
          <q-card
            v-if="postRatingGroupValidation"
            class="my-card"
            style="width: 100%; margin: 8px 0px"
          >
            <q-expansion-item separator style="padding-left: 16px">
              <template v-slot:header>
                <q-item-section avatar>
                  <q-icon color="primary" name="group" size="30px" />
                </q-item-section>

                <q-item-section> Group members' Info </q-item-section>
              </template>

              <div>
                <q-card
                  v-for="(member, member_id) in membersInfo"
                  :key="member_id"
                  style="
                    padding: 0px 0px 0px 0px;
                    margin-bottom: 8px;
                    margin-left: -16px;
                  "
                >
                  <div>
                    <q-list bordered class="rounded-borders" separator>
                      <q-item style="padding-left: 6px; padding-right: 0px">
                        <q-item-section avatar>
                          <q-icon
                            name="account_circle"
                            color="green"
                            size="xxs"
                          />
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          Name
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          {{ member["name"] }}
                        </q-item-section>
                      </q-item>
                      <q-item style="padding-left: 6px; padding-right: 0px">
                        <q-item-section avatar>
                          <q-icon name="elderly" color="green" size="xxs" />
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          Age
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          {{ member["age"] }}
                        </q-item-section>
                      </q-item>
                      <q-item style="padding-left: 6px; padding-right: 0px">
                        <q-item-section avatar>
                          <q-icon
                            v-if="member['gender'] === 'Male'"
                            name="man_2"
                            color="green"
                            size="xxs"
                          />
                          <q-icon
                            v-else
                            name="woman_2"
                            color="green"
                            size="xxs"
                          />
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          Gender
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          {{ member["gender"] }}
                        </q-item-section>
                      </q-item>
                      <q-item
                        v-if="member['cuisine'].length > 0"
                        style="padding-left: 6px; padding-right: 0px"
                      >
                        <q-item-section avatar>
                          <q-icon name="set_meal" color="green" size="xxs" />
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          Preferred cuisine
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          <span
                            v-for="(cusi, index) in member['cuisine']"
                            :key="index"
                          >
                            {{ cusi.toUpperCase() }}
                          </span>
                        </q-item-section>
                      </q-item>
                      <q-item
                        v-if="member['preference'].length > 0"
                        style="padding-left: 6px; padding-right: 0px"
                      >
                        <q-item-section avatar>
                          <q-icon name="fastfood" color="green" size="xxs" />
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          Preferred preferences
                        </q-item-section>
                        <q-item-section style="padding-right: 0px">
                          <span
                            v-for="(dish, index) in member['preference']"
                            :key="index"
                          >
                            {{ food_name_change(dish) }}
                          </span>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                </q-card>
              </div></q-expansion-item
            >
          </q-card>
        </div>
        <div v-for="(rest, index) in nextRest" :key="index">
          <!-- <q-card class="my-card" style="width: 100%; margin: auto">
            <q-card-section>
              <p style="color: red; font-weight: bold">
                {{ postRatingMassege }}
              </p>
            </q-card-section>
          </q-card> -->
          <div
            class="card-position q-pa-md row items-start q-gutter-md"
            style="
              margin: 8px 0px 0px 0px;
              padding-left: 0px;
              padding-right: 0px;
            "
          >
            <q-card class="my-card" style="width: 100%; margin: auto">
              <q-card-section>
                <q-img
                  :src="getLogo(rest.logo)"
                  style="height: 200px; padding: 2px; border-radius: 5px"
                />
                <q-card-section style="padding: 5px">
                  <q-rating
                    v-model="ratingModel"
                    size="2em"
                    color="yellow-8"
                    icon="star_border"
                    icon-selected="star"
                  />
                  <p style="font-weight: bold; margin-bottom: 1px">
                    {{ rest.name }}
                  </p>
                  <p style="margin-bottom: 1px">Address: {{ rest.address }}</p>
                  <p style="padding-bottom: 2px; margin-bottom: 0px">
                    <a
                      :href="links[rest.name]"
                      style="text-decoration: none"
                      target="_blank"
                      ><b>Link</b></a
                    >
                  </p>
                  <q-list class="rounded-borders">
                    <q-expansion-item
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
                          :label="
                            food_name_change(category) +
                            ' (' +
                            String(foodList.length) +
                            ')'
                          "
                        >
                          <div class="q-pa-md" style="width: 100%">
                            <div
                              v-for="(food, indexIn) in foodList"
                              :key="indexIn"
                            >
                              <q-list>
                                <q-item clickable v-ripple>
                                  <q-item-section>{{ food }}</q-item-section>
                                </q-item>
                              </q-list>
                              <q-separator />
                            </div>
                          </div>
                        </q-expansion-item>
                      </div>
                    </q-expansion-item>
                  </q-list>
                </q-card-section>
                <div class="parent">
                  <q-btn
                    label="Submit and Next"
                    type="submit"
                    @click="
                      ratedPost(rest.id, index, Object.keys(nextRest).length)
                    "
                    color="primary"
                  />
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
      </div>
      <q-btn
        color="green"
        style="bottom: 0; position: fixed; margin-bottom: 16px"
        @click="signOut()"
        >Sign out</q-btn
      >
    </div>
  </div>
</template>

<script>
import { defineComponent } from "vue";
import { ref } from "vue";
import axios from "axios";
import Vue from "vue";
import VueCookies from "vue-cookies";

export default {
  emits: ["nameDedicated", "userIdDictated", "stepEmit"],
  props: ["itemSelected", "groupConstructedValidator"],
  data() {
    return {
      indiviualMaxNum: 0,
      groupRatingMaxProgress: 0,
      groupRatingMaxProgressCheck: false,
      progressPost: ref(0),
      postRatingActive: false,
      itemSelectedHere: false,
      french: ref(false),
      chinese: ref(false),
      jpan: ref(false),
      italian: ref(false),
      greek: ref(false),
      indian: ref(false),
      spain: ref(false),
      lebanan: ref(false),
      moroccan: ref(false),
      turkish: ref(false),
      thai: ref(false),
      postRatingMassege:
        "Please rate the following restaurant bases on your <b>PERSONAL PREFERENCE</b>.",
      postRatingStatus: "individual",
      step: ref(1),
      progressCounter: 0,
      restLength: 0,
      progress: ref(0),
      menuList: {},
      ratingModel: ref(0),
      nextRest: [],
      links: require(`../assets/external_link.json`),
      restaurantJsonRel: [],
      individualAttractiveness: {},
      PASTAModel: ref(false),
      CARNEModel: ref(false),
      RISOModel: ref(false),
      PIZZAModel: ref(false),
      PESCEModel: ref(false),
      FUNGHIModel: ref(false),
      VERDUREModel: ref(false),
      TORTELLINIModel: ref(false),
      FORMAGGIModel: ref(false),
      CROSTACEI_E_MOLLUSCHIModel: ref(false),
      GNOCCHIModel: ref(false),
      LEGUMIModel: ref(false),
      genderModel: ref(null),
      ageModel: ref(25),
      countryModel: ref("Italy"),
      name: "",
      email: "",
      password: "",
      signPage: ref("in"),
      signed: false,
      accept: ref(false),
      submittedName: "",
      infoValidation: false,
      ratingValidation: false,
      userId: -1,
      genderOption: ["Female", "Male"],
      ageOption: [
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
        20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37,
        38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55,
        56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73,
        74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
        92, 93, 94, 95, 96, 97, 98, 99, 100,
      ],
      countryOption: [
        "Afghanistan",
        "Albania",
        "Algeria",
        "American Samoa",
        "Andorra",
        "Angola",
        "Anguilla",
        "Antarctica",
        "Antigua",
        "Argentina",
        "Armenia",
        "Aruba",
        "Australia",
        "Austria",
        "Azerbaijan",
        "Bahamas (the)",
        "Bahrain",
        "Bangladesh",
        "Barbados",
        "Belarus",
        "Belgium",
        "Belize",
        "Benin",
        "Bermuda",
        "Bhutan",

        "Bosnia",
        "Botswana",
        "Bouvet Island",
        "Brazil",

        "Brunei",
        "Bulgaria",
        "Burkina Faso",
        "Burundi",
        "Cabo Verde",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Cayman ",
        "Central African",
        "Chad",
        "Chile",
        "China",
        "Christmas Island",
        "Cocos ",
        "Colombia",
        "Comoros ",
        "Congo ",
        "Congo ",
        "Cook Islands ",
        "Costa Rica",
        "Croatia",
        "Cuba",
        "Curaçao",
        "Cyprus",
        "Czechia",
        "Côte d'Ivoire",
        "Denmark",
        "Djibouti",
        "Dominica",
        "Dominican Republic",
        "Ecuador",
        "Egypt",
        "El Salvador",
        "Equatorial Guinea",
        "Eritrea",
        "Estonia",
        "Eswatini",
        "Ethiopia",
        "Faroe Islands ",
        "Fiji",
        "Finland",
        "France",
        "French Guiana",
        "French Polynesia",
        "Gabon",
        "Gambia",
        "Georgia",
        "Germany",
        "Ghana",
        "Gibraltar",
        "Greece",
        "Greenland",
        "Grenada",
        "Guadeloupe",
        "Guam",
        "Guatemala",
        "Guernsey",
        "Guinea",
        "Guinea-Bissau",
        "Guyana",
        "Haiti",
        "Holy See (the)",
        "Honduras",
        "Hong Kong",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Iran",
        "Iraq",
        "Ireland",
        "Isle of Man",
        "Israel",
        "Italy",
        "Jamaica",
        "Japan",
        "Jersey",
        "Jordan",
        "Kazakhstan",
        "Kenya",
        "Kiribati",
        "Korea",
        "Kuwait",
        "Kyrgyzstan",
        "Latvia",
        "Lebanon",
        "Lesotho",
        "Liberia",
        "Libya",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Macao",
        "Madagascar",
        "Malawi",
        "Malaysia",
        "Maldives",
        "Mali",
        "Malta",
        "Marshall Islands ",
        "Martinique",
        "Mauritania",
        "Mauritius",
        "Mayotte",
        "Mexico",
        "Monaco",
        "Mongolia",
        "Montenegro",
        "Montserrat",
        "Morocco",
        "Mozambique",
        "Myanmar",
        "Namibia",
        "Nauru",
        "Nepal",
        "Netherlands",
        "New Caledonia",
        "New Zealand",
        "Nicaragua",
        "Niger",
        "Nigeria",
        "Niue",
        "Norfolk Island",
        "Norway",
        "Oman",
        "Pakistan",
        "Palau",
        "Palestine",
        "Panama",
        "Papua New",
        "Paraguay",
        "Peru",
        "Philippines ",
        "Pitcairn",
        "Poland",
        "Portugal",
        "Puerto Rico",
        "Qatar",
        "Macedonia",
        "Romania",
        "Russian",
        "Rwanda",
        "Réunion",
        "Saint Barthélemy",
        "Saint",
        "Saint Lucia",
        "Saint Martin",
        "Samoa",
        "San Marino",
        "Saudi Arabia",
        "Senegal",
        "Serbia",
        "Seychelles",
        "Sierra Leone",
        "Singapore",
        "Sint Maarten",
        "Slovakia",
        "Slovenia",
        "Solomon Islands",
        "Somalia",
        "South Africa",
        "South Georgia",
        "South Sudan",
        "Spain",
        "Sri Lanka",
        "Sudan (the)",
        "Suriname",
        "Sweden",
        "Switzerland",
        "Syrian Arab",
        "Taiwan",
        "Tajikistan",
        "Tanzania",
        "Thailand",
        "Timor-Leste",
        "Togo",
        "Tokelau",
        "Tonga",
        "Trinidad",
        "Tunisia",
        "Turkey",
        "Turkmenistan",
        "Tuvalu",
        "Uganda",
        "Ukraine",
        "United Arab",
        "United Kingdom ",
        "United States",
        "Uruguay",
        "Uzbekistan",
        "Vanuatu",
        "Venezuela ",
        "Viet Nam",
        "Virgin",
        "Wallisa",
        "Western ",
        "Yemen",
        "Zambia",
        "Zimbabwe",
      ],
      shortendLength: 0,
      postRatingGroupRest: [],
      postRatingindividualRest: [],
      individualCounter: 0,
      postRatingGroupValidation: false,
      postRatingMassegeWaitning:
        "You have selected the restaurant. Now, please rate the restaurant that the system shows you and fill out the questionnaire. They will appear on the screen in a few seconds.",
    };
  },
  watch: {
    itemSelected() {
      if (this.itemSelected === true) {
        this.itemSelectedHere = true;
        var progressUpdate = {
          user_id: this.userId,
          column_name: "decision_making",
          decision_making: true,
        };
        axios
          .post("http://46.18.25.97:8050/user/update/progress", progressUpdate)
          .then((response) => {
            if (this.membersInfo !== "Wait for your group.") {
              this.step = ref(3);
              this.postRating();
            }
          });
      }
    },
    groupConstructedValidator() {
      if (
        this.groupConstructedValidator === true &&
        this.itemSelectedHere === false
      ) {
        this.step = ref(2);
      }
    },
  },
  methods: {
    postRating() {
      if (this.userId >= 0) {
        var urlmnue =
          "http://46.18.25.97:8050/user/restaurant/waiting/check/" +
          String(this.userId);
        axios.get(urlmnue).then((response) => {
          if (response.data === true) {
            var urlmnue =
              "http://46.18.25.97:8050/user/restaurant/individual/rating/" +
              String(this.userId);
            axios.get(urlmnue).then((response) => {
              this.postRatingindividualRest = response.data;
              this.restPostIndividualRating({});
            });
          } else {
            this.postRatingMassegeWaitning =
              "You have selected the restaurant. Please wait for the rest of the organizers to make their decisions.";
          }
        });
      }
    },
    getLogo(logo) {
      return require(`../assets/logo/` + String(logo));
    },
    food_name_change(food_name) {
      if (food_name === "FORMAGGI") {
        return "CHEESE";
      } else if (food_name === "VERDURE") {
        return "SALAD";
      } else if (food_name === "FUNGHI") {
        return "MASHROOM";
      } else if (food_name === "PESCE") {
        return "FISH";
      } else if (food_name === "RISO") {
        return "RICE";
      } else if (food_name === "CARNE") {
        return "RED MEAT";
      } else if (food_name === "CROSTACEI_E_MOLLUSCHI") {
        return "BURGER";
      } else if (food_name === "GNOCCHI") {
        return "SOUP";
      } else if (food_name === "CARNE") {
        return "RED MEAT";
      } else if (food_name === "TORTELLINI") {
        return "WHITE MEAT";
      } else if (food_name === "LEGUMI") {
        return "CHINESE NOODLE";
      } else {
        return food_name;
      }
    },
    signOut() {
      this.signed = false;
      this.userId = -1;
      this.submittedName = 0;
      this.$emit("nameDedicated", "Guest");
      sessionStorage.clear();
      if ($cookies.isKey("email")) {
        $cookies.remove("email");
      }
      if ($cookies.isKey("password")) {
        $cookies.remove("password");
      }
      setTimeout(function () {
        location.reload();
      }, 1000);
    },
    onSubmit(status) {
      if (status === "up") {
        if (this.accept !== true) {
          this.$q.notify({
            color: "red-5",
            textColor: "white",
            icon: "warning",
            message: "You need to accept the license and terms first",
          });
        } else {
          var user = {
            id: sessionStorage.getItem("userInfo"),
            name: this.name,
            email: this.email,
            password: this.password,
          };
          this.userId = sessionStorage.getItem("userInfo");
          axios
            .post("http://46.18.25.97:8050/registration", user)
            .then((response) => {
              var massage = response.data;
              if (
                massage ===
                "You have previously submitted to the system with this email"
              ) {
                this.$q.notify({
                  color: "red-4",
                  textColor: "white",
                  icon: "cloud_done",
                  message: massage,
                });
              } else {
                this.submittedName = this.name;
                this.$emit("nameDedicated", this.name);
                this.$q.notify({
                  color: "green-4",
                  textColor: "white",
                  icon: "cloud_done",
                  message: massage,
                });
                this.userId = sessionStorage.getItem("userInfo");
                const urlmnue =
                  "http://46.18.25.97:8050/user/set/progress/" +
                  String(this.userId);
                axios.get(urlmnue).then((response) => {
                  var accountProgress = JSON.parse(
                    JSON.stringify(response.data)
                  );
                  $cookies.set("email", this.email);
                  $cookies.set("password", this.password);
                  this.signed = true;
                });
              }
            });
        }
      } else {
        var user = {
          email: this.email,
          password: this.password,
        };
        axios.post("http://46.18.25.97:8050/login", user).then((response) => {
          var massage = JSON.parse(JSON.stringify(response.data));
          this.submittedName = Object.values(massage)[0];
          this.userId = Object.keys(massage)[0];
          if (typeof massage !== "object") {
            this.$q.notify({
              color: "red-4",
              textColor: "white",
              icon: "cloud_done",
              message: massage,
            });
          } else {
            this.$emit("userIdDictated", massage);
            this.$q.notify({
              color: "green-4",
              textColor: "white",
              icon: "cloud_done",
              message: "You logged in successfully",
            });

            const urlmnue =
              "http://46.18.25.97:8050/user/get/progress/" +
              String(this.userId);
            axios.get(urlmnue).then((response) => {
              var currentStep = response.data;
              var accountProgress = JSON.parse(JSON.stringify(response.data));
              this.infoValidation =
                accountProgress["personal_info"] === 0 ? false : true;
              this.ratingValidation =
                accountProgress["pre_rating"] === 0 ? false : true;
              if (this.ratingValidation) {
                this.step = ref(1);
              }
              if (this.infoValidation && !this.ratingValidation) {
                this.restRating();
              }
              $cookies.set("email", this.email);
              $cookies.set("password", this.password);
              const url =
                "http://46.18.25.97:8050/user/get/group/" + String(this.userId);
              axios.get(url).then((response) => {
                this.membersInfo = response.data;
                if (this.membersInfo !== "Wait for your group.") {
                  this.step = ref(2);
                }
                // else {
                //   this.step = ref(3);
                // }
                if (
                  !currentStep["post_rating"] &&
                  currentStep["decision_making"]
                ) {
                  if (this.membersInfo !== "Wait for your group.") {
                    this.step = ref(3);
                    this.itemSelectedHere = true;
                    this.postRating();
                  }
                }
                if (currentStep["post_rating"]) {
                  this.step = ref(4);
                  this.$emit("stepEmit");
                }
              });
              this.signed = true;
            });
          }
        });
      }
    },
    onReset() {
      if (status === "up") {
        this.name.value = null;
        this.email.value = null;
        this.password.value = null;
        this.accept.value = false;
      } else {
      }
    },
    onSubmitUserInfo() {
      var preferenceCategoryList = [
        this.PASTAModel,
        this.CARNEModel,
        this.RISOModel,
        this.PIZZAModel,
        this.PESCEModel,
        this.FUNGHIModel,
        this.VERDUREModel,
        this.TORTELLINIModel,
        this.FORMAGGIModel,
        this.CROSTACEI_E_MOLLUSCHIModel,
        this.GNOCCHIModel,
        this.LEGUMIModel,
      ];
      const count = preferenceCategoryList.filter(Boolean).length;

      var cuisineList = [
        this.french,
        this.chinese,
        this.jpan,
        this.italian,
        this.greek,
        this.indian,
        this.spain,
        this.lebanan,
        this.moroccan,
        this.turkish,
        this.thai,
      ];
      const countCuisine = cuisineList.filter(Boolean).length;

      if (count === 0) {
        this.$q.notify({
          color: "red-4",
          textColor: "white",
          icon: "cloud_done",
          message: "Please select a number of dishes as you favorite foods.",
        });
      } else {
        if (countCuisine === 0) {
          this.$q.notify({
            color: "red-4",
            textColor: "white",
            icon: "cloud_done",
            message: "Please select a number of cuisine that you like.",
          });
        } else {
          if (this.genderModel === null) {
            this.$q.notify({
              color: "red-4",
              textColor: "white",
              icon: "cloud_done",
              message: "Please specify your gender.",
            });
          } else {
            if (this.ageModel === null) {
              this.$q.notify({
                color: "red-4",
                textColor: "white",
                icon: "cloud_done",
                message: "Please insert your age.",
              });
            } else {
              if (this.countryModel === null) {
                this.$q.notify({
                  color: "red-4",
                  textColor: "white",
                  icon: "cloud_done",
                  message: "Please insert your nationality.",
                });
              } else {
                var userInfoVar = {
                  user_id: this.userId,
                  gender: this.genderModel,
                  nationality: this.countryModel,
                  age: this.ageModel,
                  TORTELLINI: this.TORTELLINIModel,
                  PESCE: this.PESCEModel,
                  CARNE: this.CARNEModel,
                  GNOCCHI: this.GNOCCHIModel,
                  PIZZA: this.PIZZAModel,
                  RISO: this.RISOModel,
                  FORMAGGI: this.FORMAGGIModel,
                  LEGUMI: this.LEGUMIModel,
                  VERDURE: this.VERDUREModel,
                  INTERIORA: false,
                  FUNGHI: this.FUNGHIModel,
                  CROSTACEI_E_MOLLUSCHI: this.CROSTACEI_E_MOLLUSCHIModel,
                  PASTA: this.PASTAModel,
                  SALUMI: false,
                  french: this.french,
                  chinese: this.chinese,
                  jpan: this.jpan,
                  italian: this.italian,
                  greek: this.greek,
                  indian: this.indian,
                  spain: this.spain,
                  lebanan: this.lebanan,
                  moroccan: this.moroccan,
                  turkish: this.turkish,
                  thai: this.thai,
                };
                axios
                  .post("http://46.18.25.97:8050/setuserinfo", userInfoVar)
                  .then((response) => {
                    var massage = response.data;
                    if (massage !== true) {
                      this.$q.notify({
                        color: "red-4",
                        textColor: "white",
                        icon: "cloud_done",
                        message:
                          "Your data have not been submitted successfully.",
                      });
                    } else {
                      this.$q.notify({
                        color: "green-4",
                        textColor: "white",
                        icon: "cloud_done",
                        message: "Data has been submitted.",
                      });
                    }
                    var userPrefInfo = {
                      user_id: this.userId,
                      TORTELLINI: this.TORTELLINIModel,
                      PESCE: this.PESCEModel,
                      CARNE: this.CARNEModel,
                      GNOCCHI: this.GNOCCHIModel,
                      PIZZA: this.PIZZAModel,
                      RISO: this.RISOModel,
                      FORMAGGI: this.FORMAGGIModel,
                      LEGUMI: this.LEGUMIModel,
                      VERDURE: this.VERDUREModel,
                      INTERIORA: false,
                      FUNGHI: this.FUNGHIModel,
                      CROSTACEI_E_MOLLUSCHI: this.CROSTACEI_E_MOLLUSCHIModel,
                      PASTA: this.PASTAModel,
                      SALUMI: false,
                    };
                    axios
                      .post("http://46.18.25.97:8050/preferences", userPrefInfo)
                      .then((response) => {
                        this.infoValidation = true;
                        this.restRating();
                      });
                  });
              }
            }
          }
        }
      }
    },
    restRating() {
      axios
        .get(
          "http://46.18.25.97:8050/individual/attractiveness/" +
            String(this.userId)
        )
        .then((response) => {
          this.individualAttractiveness = JSON.parse(
            JSON.stringify(response.data)
          );
          var attractiveRestuarants = Object.values(
            this.individualAttractiveness
          )[0];
          var counterLoop = 0;
          this.restLength = Object.keys(attractiveRestuarants).length;
          var restToRate = Object.keys(attractiveRestuarants);
          var j, x, i;
          for (i = restToRate.length - 1; i > 0; i--) {
            j = Math.floor(Math.random() * (i + 1));
            x = restToRate[i];
            restToRate[i] = restToRate[j];
            restToRate[j] = x;
          }
          restToRate = restToRate.slice(0, Math.min(10, this.restLength));
          this.shortendLength = restToRate.length;
          for (var rest of restToRate) {
            axios
              .get("http://46.18.25.97:8050/restaurant/" + String(rest))
              .then((response) => {
                this.restaurantJsonRel.push(
                  JSON.parse(JSON.stringify(response.data))
                );
                counterLoop = counterLoop + 1;
                if (counterLoop === restToRate.length) {
                  this.nextRest.push(this.restaurantJsonRel[0]);
                  const urlmnue =
                    "http://46.18.25.97:8050/restaurant/menu/" +
                    String(this.restaurantJsonRel[0].id);
                  axios.get(urlmnue).then((response) => {
                    this.menuList = JSON.parse(JSON.stringify(response.data));
                  });
                  this.restaurantJsonRel = this.restaurantJsonRel.splice(1);
                  var progressUpdate = {
                    user_id: this.userId,
                    column_name: "personal_info",
                    personal_info: true,
                  };
                  axios
                    .post(
                      "http://46.18.25.97:8050/user/update/progress",
                      progressUpdate
                    )
                    .then((response) => {
                      // this.menuList = JSON.parse(JSON.stringify(response.data));
                    });
                }
              });
          }
        });
    },
    // restPostRating(restaurantList) {
    //   for (var rest of Object.keys(attractiveRestuarants)) {
    //     axios
    //       .get("http://46.18.25.97:8050/restaurant/" + String(rest))
    //       .then((response) => {
    //         this.restaurantJsonRel.push(
    //           JSON.parse(JSON.stringify(response.data))
    //         );
    //         counterLoop = counterLoop + 1;
    //         if (counterLoop === this.restLength) {
    //           this.nextRest.push(this.restaurantJsonRel[0]);
    //           const urlmnue =
    //             "http://46.18.25.97:8050/restaurant/menu/" +
    //             String(this.restaurantJsonRel[0].id);
    //           axios.get(urlmnue).then((response) => {
    //             this.menuList = JSON.parse(JSON.stringify(response.data));
    //           });
    //           this.restaurantJsonRel = this.restaurantJsonRel.splice(1);
    //         }
    //       });
    //   }
    // },
    restPostGroupRating(restaurantList) {
      this.postRatingMassege =
        "Please rate the following restaurant with respect to the <b>GROUP PREFERENCES</b>";
      this.postRatingGroupValidation = true;
      var restLengthGroup = restaurantList.length;
      var counterLoop = 0;
      for (var rest of Object.values(restaurantList)) {
        axios
          .get("http://46.18.25.97:8050/restaurant/" + String(rest))
          .then((response) => {
            this.restaurantJsonRel.push(
              JSON.parse(JSON.stringify(response.data))
            );
            counterLoop = counterLoop + 1;
            if (counterLoop === restLengthGroup) {
              this.nextRest.push(this.restaurantJsonRel[0]);
              const urlmnue =
                "http://46.18.25.97:8050/restaurant/menu/" +
                String(this.restaurantJsonRel[0].id);
              axios.get(urlmnue).then((response) => {
                this.menuList = JSON.parse(JSON.stringify(response.data));
              });
              this.restaurantJsonRel = this.restaurantJsonRel.splice(1);
            }
            this.postRatingActive = true;
          });
      }
    },
    restPostIndividualRating(restaurantList) {
      var urlmnue =
        "http://46.18.25.97:8050/user/restaurant/group/rating/" +
        String(this.userId);
      axios.get(urlmnue).then((response) => {
        restaurantList = response.data;

        // const reversedKeys = Object.keys(restaurantList).reverse();
        var maxNum = Math.min(Object.keys(restaurantList).length, 10);
        this.indiviualMaxNum = maxNum;
        this.progressCounter = 0;
        var restLengthindividual = restaurantList.length;
        var counterLoop = 0;
        if (restaurantList.length !== 0) {
          this.postIndividualFlag = true;
          var counting = 0;
          for (var rest of Object.values(restaurantList).reverse()) {
            counting++;
            if (counting <= maxNum) {
              axios
                .get("http://46.18.25.97:8050/restaurant/" + String(rest))
                .then((response) => {
                  this.restaurantJsonRel.push(
                    JSON.parse(JSON.stringify(response.data))
                  );
                  counterLoop = counterLoop + 1;
                  if (counterLoop === maxNum) {
                    this.nextRest.push(this.restaurantJsonRel[0]);
                    const urlmnue =
                      "http://46.18.25.97:8050/restaurant/menu/" +
                      String(this.restaurantJsonRel[0].id);
                    axios.get(urlmnue).then((response) => {
                      this.menuList = JSON.parse(JSON.stringify(response.data));
                    });
                    this.restaurantJsonRel = this.restaurantJsonRel.splice(1);
                  }
                });
            }
          }
        } else {
          this.restaurantJsonRel = {};
        }
      });
    },
    onResetUserInfo() {
      this.PASTAModel = ref(false);
      this.CARNEModel = ref(false);
      this.RISOModel = ref(false);
      this.PIZZAModel = ref(false);
      this.PESCEModel = ref(false);
      this.FUNGHIModel = ref(false);
      this.VERDUREModel = ref(false);
      this.TORTELLINIModel = ref(false);
      this.FORMAGGIModel = ref(false);
      this.CROSTACEI_E_MOLLUSCHIModel = ref(false);
      this.GNOCCHIModel = ref(false);
      this.LEGUMIModel = ref(false);
      this.genderModel = ref(null);
      this.ageModel = ref(25);
      this.countryModel = ref("Italy");
    },
    rated(restId, index) {
      if (this.ratingModel > 0) {
        if (this.progressCounter >= this.shortendLength - 1) {
          var progressUpdate = {
            user_id: this.userId,
            column_name: "pre_rating",
            pre_rating: true,
          };
          axios
            .post(
              "http://46.18.25.97:8050/user/update/progress",
              progressUpdate
            )
            .then((response) => {
              // this.menuList = JSON.parse(JSON.stringify(response.data));
            });
          this.ratingValidation = true;
        } else {
          var user_rating = {
            user_id: this.userId,
            restaurant_id: restId,
            rating: this.ratingModel,
            group: false,
          };
          this.ratingModel = ref(0);
          axios
            .post("http://46.18.25.97:8050/user/pre/rating", user_rating)
            .then((response) => {
              // this.menuList = JSON.parse(JSON.stringify(response.data));
            });
          this.progressCounter = this.progressCounter + 1;
          if (this.step < 3) {
            var progressCompleted = this.progressCounter / 10;
          } else {
            var progressCompleted = this.progressCounter / this.restLength;
          }
          this.progress = ref(progressCompleted);
          this.nextRest = [];
          this.nextRest.push(this.restaurantJsonRel[0]);
          const urlmnue =
            "http://46.18.25.97:8050/restaurant/menu/" +
            String(this.restaurantJsonRel[0].id);
          axios.get(urlmnue).then((response) => {
            this.menuList = JSON.parse(JSON.stringify(response.data));
          });
          this.restaurantJsonRel = this.restaurantJsonRel.splice(1);
          this.$q.notify({
            color: "green-4",
            textColor: "white",
            icon: "cloud_done",
            message: "Rating submitted.",
          });
        }
      } else {
        this.$q.notify({
          color: "red-4",
          textColor: "white",
          icon: "cloud_done",
          message: "Please Rate the restaurant.",
        });
      }
    },
    ratedPost(restId, index, length) {
      if (this.groupRatingMaxProgressCheck === false) {
        var maxNum = this.indiviualMaxNum;
      } else {
        var maxNum = this.groupRatingMaxProgress;
      }
      // if (this.groupRatingMaxProgressCheck && this.progressCounter > maxNum) {
      //   var progressUpdate = {
      //     user_id: this.userId,
      //     column_name: "post_rating",
      //     post_rating: true,
      //   };
      //   axios
      //     .post("http://46.18.25.97:8050/user/update/progress", progressUpdate)
      //     .then((response) => {
      //       this.menuList = JSON.parse(JSON.stringify(response.data));
      //     });
      // }
      if (this.ratingModel > 0) {
        if (
          this.restaurantJsonRel.length === 0 &&
          this.postRatingStatus === "group"
        ) {
          var progressUpdate = {
            user_id: this.userId,
            column_name: "post_rating",
            post_rating: true,
          };
          axios
            .post(
              "http://46.18.25.97:8050/user/update/progress",
              progressUpdate
            )
            .then((response) => {
              // this.menuList = JSON.parse(JSON.stringify(response.data));
            });
          var user_rating = {
            user_id: this.userId,
            restaurant_id: restId,
            rating: this.ratingModel,
            group: this.groupRatingMaxProgressCheck,
          };
          this.ratingModel = ref(0);
          axios
            .post("http://46.18.25.97:8050/user/post/rating", user_rating)
            .then((response) => {
              // this.menuList = JSON.parse(JSON.stringify(response.data));
            });
          this.progressCounter = this.progressCounter + 1;
          var progressCompleted = this.progressCounter / maxNum;
          this.progressPost = ref(1);
          this.step = ref(4);
          this.$emit("stepEmit");
          this.nextRest = {};
        } else {
          var user_rating = {
            user_id: this.userId,
            restaurant_id: restId,
            rating: this.ratingModel,
            group: this.groupRatingMaxProgressCheck,
          };
          this.ratingModel = ref(0);
          axios
            .post("http://46.18.25.97:8050/user/post/rating", user_rating)
            .then((response) => {});
          // const urlmnue1 =
          //   "http://46.18.25.97:8050/restaurant/menu/" +
          //   String(this.restaurantJsonRel[0].id);
          // axios.get(urlmnue1).then((response) => {
          //   this.menuList = JSON.parse(JSON.stringify(response.data));
          // });
          this.progressCounter = this.progressCounter + 1;
          var progressCompleted = this.progressCounter / maxNum;
          this.progressPost = ref(progressCompleted);
          this.nextRest = [];
          if (this.restaurantJsonRel.length > 0) {
            this.nextRest.push(this.restaurantJsonRel[0]);
            const urlmnue =
              "http://46.18.25.97:8050/restaurant/menu/" +
              String(this.restaurantJsonRel[0].id);
            axios.get(urlmnue).then((response) => {
              this.menuList = JSON.parse(JSON.stringify(response.data));
            });
            this.restaurantJsonRel = this.restaurantJsonRel.splice(1);
          } else {
            this.postRatingStatus = "group";
            var urlmnue =
              "http://46.18.25.97:8050/user/restaurant/group/rating/" +
              String(this.userId);

            axios.get(urlmnue).then((response) => {
              this.postRatingGroupRest = response.data;
              this.progressCounter = 0;
              this.groupRatingMaxProgress = this.postRatingGroupRest.length;
              this.groupRatingMaxProgressCheck = true;
              this.progressPost = ref(0);
              this.restPostGroupRating(this.postRatingGroupRest);
            });
          }
          this.$q.notify({
            color: "green-4",
            textColor: "white",
            icon: "cloud_done",
            message: "Rating submitted.",
          });
        }
      } else {
        this.$q.notify({
          color: "red-4",
          textColor: "white",
          icon: "cloud_done",
          message: "Please Rate the restaurant.",
        });
      }
    },
  },
  mounted() {
    $cookies.set("hanif", "hanif");
    if ($cookies.isKey("email") && $cookies.isKey("password")) {
      this.email = $cookies.get("email");
      this.password = $cookies.get("password");
      this.onSubmit("in");
    }
  },
};
</script>
<style scoped>
.required:active {
  border-color: blue;
}
.required {
  border-color: red;
}
</style>
