<template>
  <div>
    <!-- <q-banner
      dense
      class="text-white bg-primary"
      style="
        display: inline-block;
        text-align: justify;
        border-radius: 6px;
        margin-top: 3px;
        margin-bottom: 3px;
        margin-right: 3px;
        margin-left: 3px;
      "
    >
      <p style="margin-bottom: 0px">
        Due to certain participants not completing the first stage of the
        experiment, it is necessary to reschedule the second stage for Monday.
        The second stage can start from Monday morning and continue until 3 PM.
        Subsequently, the final stage will begin at 4 PM on Monday and run until
        midnight.
      </p>
      <template v-slot:action>
        <q-btn
          size="sm"
          flat
          color="white"
          label="OK"
          @click="revisionBannerToggle = !revisionBannerToggle"
        />
      </template>
    </q-banner> -->
    <div
      v-if="
        pageload && pageloadbooked && popularityModelLoad && menuSizeValidity
      "
    >
      <div class="row no-wrap" style="overflow: auto" v-if="!restPageActive">
        {{ scrollToTop() }}
        <div style="display: inline-block">
          <div class="row no-wrap">
            <div @click="open()">
              <q-chip
                square
                color="primary"
                text-color="white"
                icon="import_export"
              >
                {{ sortType }}
              </q-chip>
            </div>
            <div @click="openPriceCritique()">
              <q-chip
                icon="price_change"
                square
                color="primary"
                text-color="white"
              >
                {{ getRange() }}
              </q-chip>
            </div>
            <q-separator style="margin-top: 2px; margin-bottom: 2px" />
            <div v-if="userPreferenceList.length > 0" class="row no-wrap">
              <div
                v-for="userInfoList in userPreferenceList"
                :key="userInfoList[1]"
                @click="goToGrpPage()"
              >
                <q-chip
                  square
                  :color="
                    groupInfo[userInfoList[1]][0] === 'organizer'
                      ? 'blue'
                      : groupInfo[userInfoList[1]][0]
                  "
                  text-color="white"
                >
                  {{ food_name_change(userInfoList[0]) }}
                </q-chip>
              </div>
              <q-separator style="margin-top: 2px; margin-bottom: 2px" />
            </div>
          </div>
        </div>
      </div>
      <div v-else class="row no-wrap" style="overflow: auto">
        <div style="display: inline-block">
          <div class="row no-wrap">
            <div
              v-if="!restPageActive && critiqueRange !== ''"
              @click="openPriceCritique()"
            >
              <q-chip square color="primary" text-color="white">
                {{ getRange() }}
              </q-chip>
            </div>
          </div>
        </div>
      </div>
      <!-- <q-separator style="margin-top: 2px; margin-bottom: 2px" /> -->
      <q-dialog v-model="scoreDialog">
        <q-card class="my-card" style="width: 100%">
          <div style="width: 100%; margin-left: auto">
            <q-btn icon="close" flat round dense v-close-popup />
          </div>
          <q-card-section style="height: 200px" class="card-styling">
            <div
              style="
                max-width: 100%;
                height: 200px;
                display: block;
                margin-left: auto;
                margin-right: auto;
              "
            >
              <q-img
                :src="getLogoIn(JSON.parse(restPageInfo).logo)"
                style="max-width: 100%; height: 200px"
              />
            </div>
            <q-separator style="margin: 3px 0px 3px 0px" />
          </q-card-section>
          <q-card-section class="card-styling">
            <div class="row no-wrap items-center" style="padding: 3px">
              <strong>{{ JSON.parse(restPageInfo).name }}</strong>
            </div>
            <div v-if="scoreExplanation === 'pop'">
              <div>This resturant popularity in our app</div>
              <q-rating
                v-model="popularityModel[JSON.parse(restPageInfo).id]"
                max="5"
                size="1.5em"
                color="red"
                color-selected="red-9"
                icon="favorite_border"
                icon-selected="favorite"
                icon-half="favorite"
                no-dimming
                readonly
              />
            </div>
            <div v-if="scoreExplanation === 'trip'">
              <div>TripAdvisor Score</div>
              <q-rating
                v-model="tripScore[JSON.parse(restPageInfo).id]"
                size="1.5em"
                :max="5"
                color="secondary"
                readonly
                icon="star_border"
                icon-selected="star"
                icon-half="star_half"
                no-dimming
              ></q-rating>
            </div>

            <div v-if="scoreExplanation === 'dishDiv'">
              <span style="visibility: hidden">{{
                (dishrelevancy =
                  (menuSizeRest[JSON.parse(restPageInfo).id]["dishes"] / 100) *
                  5)
              }}</span>
              <div>Dish diversity</div>
              <q-rating
                v-model="dishrelevancy"
                size="1.5em"
                :max="5"
                color="secondary"
                readonly
                icon="star_border"
                icon-selected="star"
                icon-half="star_half"
                no-dimming
              ></q-rating>
            </div>
            <div v-if="scoreExplanation === 'categ'">
              <span style="visibility: hidden">{{
                (dishrelevancy =
                  (menuSizeRest[JSON.parse(restPageInfo).id]["category"] / 10) *
                  5)
              }}</span>
              <div>Food category diversity</div>
              <q-rating
                v-model="dishrelevancy"
                size="1.5em"
                :max="5"
                color="secondary"
                readonly
                icon="star_border"
                icon-selected="star"
                icon-half="star_half"
                no-dimming
              ></q-rating>
            </div>
            <div
              v-if="
                scoreExplanation === 'avrattr' &&
                typeof avrAttractModel[JSON.parse(restPageInfo).id] !==
                  'undefined'
              "
            >
              <div>The overall fitness of this restaurant for your group</div>
              <q-rating
                v-model="avrAttractModel[JSON.parse(restPageInfo).id]"
                size="1.5em"
                :max="5"
                color="green"
                readonly
                icon="star_border"
                icon-selected="star"
                icon-half="star_half"
                no-dimming
              ></q-rating>
            </div>
            <div
              v-if="
                scoreExplanation === 'sim' &&
                typeof similarityModel[JSON.parse(restPageInfo).id] !==
                  'undefined'
              "
            >
              <div>
                Similarity to the group which bookmarked this restaurant
              </div>
              <q-rating
                v-model="similarityModel[JSON.parse(restPageInfo).id]"
                size="1.5em"
                :max="5"
                color="orange"
                readonly
                icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
              ></q-rating>
            </div>
            <div v-if="scoreExplanation === 'fair'">
              <q-rating
                v-model="fairModel[JSON.parse(restPageInfo).id]"
                size="1.5em"
                :max="5"
                color="orange"
                readonly
                icon="star_border"
                icon-selected="star"
                icon-half="star_half"
              ></q-rating>
            </div>
            <q-separator style="margin: 8px 0px 0px 0px" />
            <div
              v-if="
                scoreExplanation === 'avrattr' &&
                typeof avrAttractModel[JSON.parse(restPageInfo).id] !==
                  'undefined'
              "
              style="margin: 8px 0px 0px 0px"
            >
              <strong>Fitness for your group</strong>
            </div>
            <!-- <div
              v-if="scoreExplanation === 'fair'"
              style="margin: 8px 0px 0px 0px"
            >
              <strong>Group satisfaction equality</strong>
            </div> -->
            <div
              v-if="
                scoreExplanation === 'sim' &&
                typeof similarityModel[JSON.parse(restPageInfo).id] !==
                  'undefined'
              "
              style="margin: 8px 0px 0px 0px"
            >
              <strong
                >Similarity to the group which bookmarked this
                restaurant</strong
              >
            </div>
            <div
              v-if="scoreExplanation === 'pop'"
              style="margin: 8px 0px 0px 0px"
            >
              <strong>Popularity in our app</strong>
            </div>
          </q-card-section>
          <q-card-section class="q-pt-none" align="justify">
            <div v-if="scoreExplanation === 'trip'">
              For more information visit the restaurant's
              <a
                :href="tripPage[JSON.parse(restPageInfo).id]"
                style="text-decoration: none"
                target="_blank"
                ><b>TripAdvisor Page</b></a
              >
            </div>
            <div v-if="scoreExplanation === 'dishDiv'">
              There are
              {{ menuSizeRest[JSON.parse(restPageInfo).id]["dishes"] }} types of
              dishes in the menu of this restaurant.
            </div>
            <div v-if="scoreExplanation === 'categ'">
              There are
              {{ menuSizeRest[JSON.parse(restPageInfo).id]["category"] }}
              category of dishes in the menu of this restaurant.
            </div>
            <div
              v-if="
                scoreExplanation === 'avrattr' &&
                typeof avrAttractModel[JSON.parse(restPageInfo).id] !==
                  'undefined'
              "
              style="margin: 8px 0px 0px 0px"
            >
              Satisfaction level for
              <div
                v-for="(userAttractiveness, name, index) in attractiveness"
                :key="index"
                style="margin: 8px 0px 0px 0px"
              >
                <q-item class="memberExplan">
                  <q-item-section avatar top>
                    <q-icon
                      name="perm_identity"
                      :color="
                        groupInfo[name][0] === 'organizer'
                          ? 'primary'
                          : groupInfo[name][0]
                      "
                      size="50px"
                    />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label lines="1">
                      <span class="text-weight-medium">{{
                        groupInfo[name][1] === "Organizer"
                          ? " you"
                          : groupInfo[name][1]
                      }}</span>
                      <!-- {{ menuList }}
                           {{ userPreferenceList }}
                           {{ groupInfo }} -->
                    </q-item-label>
                    <q-item-label lines="1">
                      <q-rating
                        v-model="
                          attractivenessModel[name][JSON.parse(restPageInfo).id]
                        "
                        size="1.5em"
                        :max="5"
                        :color="
                          groupInfo[name][0] === 'organizer'
                            ? 'primary'
                            : groupInfo[name][0]
                        "
                        icon="star_border"
                        icon-selected="star"
                        icon-half="star_half"
                        no-dimming
                        readonly
                      ></q-rating
                    ></q-item-label>
                    <q-item-label caption>
                      <p>
                        {{
                          getIndiExplan(
                            menuList,
                            name,
                            groupInfo,
                            groupInfo[name][1],
                            JSON.parse(restPageInfo).id
                          )
                        }}
                      </p>
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </div>
            </div>
            <div v-if="scoreExplanation === 'fair'">
              <div
                v-if="
                  extractDissatisfiedsAbsolutNumbers(
                    JSON.parse(restPageInfo).id
                  )[1] === 'NONE'
                "
              >
                All of your group members are satisfied.
              </div>
              <div v-else>
                <div
                  v-if="
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[0] !== 'NONE'
                  "
                >
                  {{
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[0]
                  }}
                  of your group members
                  {{
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[0] === "NONE" ||
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[0] === "ONE"
                      ? "is"
                      : "are"
                  }}
                  satisfied.
                </div>
              </div>

              <div
                v-if="
                  extractDissatisfiedsAbsolutNumbers(
                    JSON.parse(restPageInfo).id
                  )[1] !== 'NONE'
                "
              >
                <div
                  v-if="
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[0] === 'NONE'
                  "
                >
                  All of you group members are not satisfied.
                </div>
                <div v-else>
                  {{
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[1]
                  }}
                  of your group members
                  {{
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[1] === "NONE" ||
                    extractDissatisfiedsAbsolutNumbers(
                      JSON.parse(restPageInfo).id
                    )[1] === "ONE"
                      ? "is"
                      : "are"
                  }}
                  not satisfied with this resturant.
                </div>
              </div>
              <div
                v-if="
                  happyValidator === true &&
                  extractDissatisfiedsAbsolutNumbers(
                    JSON.parse(restPageInfo).id
                  )[1] !== 'NONE' &&
                  extractDissatisfiedsAbsolutNumbers(
                    JSON.parse(restPageInfo).id
                  )[0] !== 'NONE'
                "
              >
                <q-separator style="margin: 2px 2px 2px 2px" />
                Satisfied members are:
                <div
                  v-for="IdOfUsers in Object.keys(userAttractive)"
                  :key="IdOfUsers"
                >
                  <div v-if="userAttractive[IdOfUsers][1] === 1">
                    <q-icon
                      size="md"
                      name="sentiment_satisfied"
                      :color="userAttractive[IdOfUsers][0]"
                    />
                    {{ userAttractive[IdOfUsers][2] }}
                  </div>
                </div>
              </div>
              <div
                v-if="
                  sadValidator === true &&
                  extractDissatisfiedsAbsolutNumbers(
                    JSON.parse(restPageInfo).id
                  )[1] !== 'NONE' &&
                  extractDissatisfiedsAbsolutNumbers(
                    JSON.parse(restPageInfo).id
                  )[0] !== 'NONE'
                "
              >
                <q-separator style="margin: 4px 4px 4px 4px" />
                Dissatisfied members are:
                <div
                  v-for="IdOfUsers in Object.keys(userAttractive)"
                  :key="IdOfUsers"
                >
                  <div v-if="userAttractive[IdOfUsers][1] === -1">
                    <q-icon
                      size="md"
                      name="sentiment_dissatisfied"
                      :color="userAttractive[IdOfUsers][0]"
                    />
                    {{ userAttractive[IdOfUsers][2] }}
                  </div>
                </div>
              </div>
            </div>
            <div
              v-if="
                scoreExplanation === 'sim' &&
                typeof similarityModel[JSON.parse(restPageInfo).id] !==
                  'undefined'
              "
            >
              <br />
              <div v-html="this.similarityExplanation"></div>
              <div
                v-for="(userAttractiveness, name, index) in attractiveness"
                :key="index"
                style="margin: 8px 0px 0px 0px"
              >
                <q-item class="memberExplan">
                  <q-item-section avatar top>
                    <q-icon
                      name="perm_identity"
                      :color="
                        groupInfo[name][0] === 'organizer'
                          ? 'primary'
                          : groupInfo[name][0]
                      "
                      size="50px"
                    />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label lines="1">
                      <span class="text-weight-medium">{{
                        groupInfo[name][1] === "Organizer"
                          ? " you"
                          : groupInfo[name][1]
                      }}</span>
                      <!-- {{ menuList }}
                           {{ userPreferenceList }}
                           {{ groupInfo }} -->
                    </q-item-label>
                    <q-item-label caption>
                      <p>
                        {{
                          getIndiExplanSim(
                            name,
                            groupInfo[name][1],
                            JSON.parse(restPageInfo).id
                          )
                        }}
                      </p>
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </div>
            </div>
            <div v-if="scoreExplanation === 'pop'">
              <div v-html="popPercentage(JSON.parse(restPageInfo).id)"></div>
            </div>
          </q-card-section>
          <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
      <q-dialog v-model="priceDialog" :position="positionPrice">
        <q-card style="width: 100%"
          ><q-list>
            <q-item clickable v-close-popup @click="price('rem')">
              <q-item-section avatar>
                <q-avatar
                  icon="highlight_off"
                  color="primary"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Remove Filter</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator style="margin-top: 2px; margin-bottom: 2px" />
            <q-item
              v-if="getRange() !== '$'"
              clickable
              v-close-popup
              @click="price('eco')"
              ><q-item-section avatar>
                <q-avatar
                  icon=" trending_down"
                  color="primary"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Economic Restaurants</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator style="margin-top: 2px; margin-bottom: 2px" />
            <q-item
              v-if="getRange() !== '$$'"
              clickable
              v-close-popup
              @click="price('mid')"
              ><q-item-section avatar>
                <q-avatar
                  icon="arrow_right_alt"
                  color="primary"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Mid-range Restaurants</q-item-label>
              </q-item-section>
            </q-item>
            <q-separator style="margin-top: 2px; margin-bottom: 2px" />
            <q-item
              v-if="getRange() !== '$$$'"
              clickable
              v-close-popup
              @click="price('exp')"
              ><q-item-section avatar>
                <q-avatar
                  icon="trending_up"
                  color="primary"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Expensive Restaurants</q-item-label>
              </q-item-section>
            </q-item>
          </q-list></q-card
        >
      </q-dialog>
      <q-dialog v-model="sortDialog" :position="position">
        <q-card style="width: 350px">
          <q-list dense>
            <q-item clickable v-close-popup @click="sorting(-1, 0, 0)">
              <q-item-section avatar>
                <q-avatar
                  icon="favorite_border"
                  color="red"
                  text-color="white"
                />
              </q-item-section>
              <q-item-section>
                <q-item-label>Sort by restaurants popularity</q-item-label>
              </q-item-section>
            </q-item>
            <div v-if="restaurantJsonRelActive">
              <q-item clickable v-close-popup @click="sorting(4, 0, 0)">
                <q-item-section avatar>
                  <q-avatar icon="groups" color="primary" text-color="white" />
                </q-item-section>
                <q-item-section>
                  <q-item-label
                    >Sort by maximizing group satisfaction</q-item-label
                  >
                </q-item-section>
              </q-item>
              <!-- <div v-for="(value, key) in groupInfo" :key="key">
                <q-item
                  clickable
                  v-close-popup
                  @click="sorting(0, key, value[1])"
                >
                  <q-item-section avatar>
                    <q-avatar
                      icon="person"
                      :color="value[0] === 'organizer' ? 'blue' : value[0]"
                      text-color="white"
                    />
                  </q-item-section>
                  <q-item-section>
                    <q-item-label
                      >Sort by
                      {{
                        String(value[1]) === "Organizer"
                          ? " your "
                          : " " + String(value[1]) + " "
                      }}
                      preference
                    </q-item-label>
                  </q-item-section>
                </q-item>
              </div> -->
              <!-- <q-item clickable v-close-popup @click="sorting(2, 0, 0)">
                <q-item-section avatar>
                  <q-avatar icon="groups" color="primary" text-color="white" />
                </q-item-section>
                <q-item-section>
                  <q-item-label
                    >Sort by fairness and attractiveness</q-item-label
                  >
                </q-item-section>
              </q-item> -->
              <!-- <q-item clickable v-close-popup @click="sorting(1, 0, 0)">
                <q-item-section avatar>
                  <q-avatar icon="groups" color="primary" text-color="white" />
                </q-item-section>
                <q-item-section>
                  <q-item-label
                    >Sort by minimizing individual dissatisfaction</q-item-label
                  >
                </q-item-section>
              </q-item> -->
              <q-item clickable v-close-popup @click="sorting(5, 0, 0)">
                <q-item-section avatar>
                  <q-avatar
                    icon="favorite_border"
                    color="primary"
                    text-color="white"
                  />
                </q-item-section>
                <q-item-section>
                  <q-item-label
                    >Sort: by Similarity to the group which bookmarked
                    restaurants</q-item-label
                  >
                </q-item-section>
              </q-item>
            </div>
          </q-list>
        </q-card>
      </q-dialog>
      <div v-show="!restPageActive">
        {{ scrollToTop() }}

        <div
          v-if="bannerToggle"
          class="q-pa-md"
          style="
            padding: 0px 0px 0px 0px;
            margin-left: 0px;
            margin-right: 0px;
            margin-top: 0px;
          "
        >
          <q-banner
            dense
            inline-actions
            class="text-white bg-red"
            style="display: inline-block; text-align: justify; width: 100%"
          >
            <p style="margin-bottom: 0px">
              There is no restaurant to make all of your group members
              satisfied. Either modify the preferences or select one of the
              following restaurants.
            </p>
            <template v-slot:action>
              <q-btn
                size="sm"
                flat
                color="white"
                label="OK"
                @click="bannerToggler()"
              />
            </template>
          </q-banner>
        </div>
        <!-- <q-page-scroller
          position="bottom-right"
          :scroll-offset="150"
          :offset="[18, 18]"
        >
          <q-btn fab icon="keyboard_arrow_up" color="primary" class="scroll" />
        </q-page-scroller> -->
        <div v-for="(rest, index) in restaurantJsonRel" :key="index">
          {{
            revisionflagToggler(
              JSON.parse(rest).id,
              extractDissatisfiedsBinary(JSON.parse(rest).id)
            )
          }}
          <!-- <div>
            For adding this functionality to other sorting method add the following piece of code to the following if
            ||
                (typeof userPreferenceList !== undefined &&
                  Object.keys(userPreferenceList).length > 0 &&
                  sortingType === 'pop' &&
                  index === 0) ||
                (typeof userPreferenceList !== undefined &&
                  Object.keys(userPreferenceList).length > 0 &&
                  sortingType === 'sim' &&
                  index === 0)</div> -->
          <div style="margin: 0px 2px">
            <q-card
              v-if="
                typeof userPreferenceList !== undefined &&
                Object.keys(userPreferenceList).length > 0 &&
                extractDissatisfiedsBinary(JSON.parse(rest).id) &&
                revisionFlag[JSON.parse(rest).id] &&
                sortingType === 'avrattr'
              "
              class="sadnessActive"
              flat
              bordered
              style="
                margin-left: 2px auto;
                margin-right: 2px auto;
                margin-bottom: 7px auto;
                padding: 2px 2px 2px 2px;
                height: auto;
                width: 100%;
              "
            >
              <q-list>
                <q-item style="padding-left: 8px; padding-right: 8px" dense>
                  <q-item-section avatar dense>
                    <q-icon
                      name="sentiment_dissatisfied"
                      color="amber-14"
                      size="xl"
                    />
                  </q-item-section>
                  <q-item-section style="padding-right: 0px">
                    <div>
                      The number of restaurants that satisfy all group members is <strong>{{ currentRestaurant }}</strong>
                    </div>
                    <q-separator style="margin: 8px 0px" />
                    To increase the number of restaurants that satisfy all group members, revise their preferences.
                  </q-item-section>
                </q-item>
                <q-item>
                  <q-item-section>
                    <div style="margin: auto">
                      <q-btn
                        size="x"
                        push
                        color="primary"
                        text-color="white"
                        label="Revise"
                        style="margin: 8px"
                        @click="RevisionBannerTogglerRevise(index)"
                      />
                    </div>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card>
          </div>
          <div
            v-if="extractDissatisfiedsBinary(JSON.parse(rest).id)"
            class="q-pa-md row items-start q-gutter-md"
            style="
              margin-left: 2px auto;
              margin-right: 2px auto;
              margin-bottom: 7px auto;
              padding: 2px 2px 2px 2px;
            "
            :id="JSON.parse(rest).id"
          >
            <q-card
              class="my-card sadnessActive"
              flat
              bordered
              style="height: auto"
            >
              <q-card-section horizontal style="cursor: pointer">
                <q-img
                  class="col-5"
                  :src="getLogo(JSON.parse(rest).logo)"
                  style="
                    padding: 2px;
                    width: 120px;
                    height: 120px;
                    cursor: pointer;
                  "
                  @click="goToRestPage(rest)"
                />
                <div
                  class="absolute"
                  style="top: 4px; left: 4px; border-radius: 25px"
                >
                  <div class="q-pa-md parent" style="padding: 5px">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="model3[JSON.parse(rest).id]"
                        max="1"
                        size="25px"
                        color="red-14"
                        color-selected="red-9"
                        icon="favorite_border"
                        icon-selected="favorite"
                        @click="submitRemoveBookmark(JSON.parse(rest).id)"
                        style="background: LavenderBlush; border-radius: 8px"
                      />
                    </div>
                  </div>
                </div>
                <q-card-section
                  style="padding: 5px; width: 100%"
                  @click="goToRestPage(rest)"
                >
                  <q-list dense>
                    <q-item
                      dense
                      style="
                        margin-top: 0px;
                        margin-bottom: 0px;
                        margin-left: 0px;
                        padding: 0px 0px 0px 0px;
                      "
                    >
                      <q-item-section
                        dense
                        style="
                          margin-top: 0px;
                          margin-bottom: 0px;
                          margin-left: 0px;
                          padding: 0px 0px 0px 0px;
                        "
                      >
                        <strong>{{ JSON.parse(rest).name }}</strong>
                      </q-item-section>
                    </q-item>
                    <q-item
                      dense
                      style="
                        margin-top: 0px;
                        margin-bottom: 0px;
                        margin-left: 0px;
                        padding: 0px 0px 0px 0px;
                      "
                      ><q-item-section>{{
                        JSON.parse(rest).address
                      }}</q-item-section></q-item
                    >
                  </q-list>
                  <div v-if="sortingType === 'pop'">
                    <q-list dense>
                      <q-item
                        dense
                        style="
                          margin-top: 0px;
                          margin-bottom: 0px;
                          margin-left: 0px;
                          padding: 0px 0px 0px 0px;
                        "
                      >
                        <q-item-section
                          dense
                          style="
                            margin-top: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            padding: 0px 0px 0px 0px;
                          "
                        >
                          Popularity
                        </q-item-section>
                        <q-item-section dense>
                          <q-rating
                            v-model="popularityModel[JSON.parse(rest).id]"
                            max="5"
                            size="1.2em"
                            color="red"
                            color-selected="red-9"
                            icon="favorite_border"
                            icon-selected="favorite"
                            icon-half="favorite"
                            no-dimming
                            readonly
                          />
                        </q-item-section>
                      </q-item>
                    </q-list>

                    <!-- <q-linear-progress
                      :value="
                        parseInt(popPercentage(JSON.parse(rest).id)) / 100
                      "
                      size="18px"
                      color="teal-3"
                      class="q-mt-sm"
                      style="width: 100%; border-radius: 15px"
                    >
                      <div class="absolute-full flex flex-center">
                        <q-badge
                          color="white"
                          text-color="accent"
                          :label="popPercentage(JSON.parse(rest).id) + '%'"
                        />
                      </div>
                    </q-linear-progress> -->
                  </div>
                  <div v-if="sortingType === 'avrattr'">
                    <q-list dense>
                      <q-item
                        dense
                        style="
                          margin-top: 0px;
                          margin-bottom: 0px;
                          margin-left: 0px;
                          padding: 0px 0px 0px 0px;
                        "
                      >
                        <q-item-section
                          dense
                          style="
                            margin-top: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            padding: 0px 0px 0px 0px;
                          "
                        >
                          Fitness for your group
                        </q-item-section>
                        <q-item-section dense>
                          <q-rating
                            v-model="avrAttractModel[JSON.parse(rest).id]"
                            size="1.2em"
                            :max="5"
                            color="green"
                            readonly
                            icon="star_border"
                            icon-selected="star"
                            icon-half="star_half"
                            no-dimming
                          ></q-rating>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                  <div
                    v-if="sortingType === 'attr'"
                    style="margin-top: 6px; margin-bottom: 6px"
                  >
                    Satisfaction level for
                    {{
                      groupInfo[sortUserId][1] === "Organizer"
                        ? " you"
                        : groupInfo[sortUserId][1]
                    }}:
                    <q-linear-progress
                      :value="attractiveness[sortUserId][JSON.parse(rest).id]"
                      :color="groupInfo[sortUserId][0]"
                      class="q-mt-sm"
                      size="18px"
                      style="width: 100%; border-radius: 15px"
                    >
                      <div class="absolute-full flex flex-center">
                        <q-badge
                          color="white"
                          text-color="accent"
                          :label="
                            parseInt(
                              parseFloat(
                                attractiveness[sortUserId][JSON.parse(rest).id]
                              ).toFixed(2) * 100
                            ) + '%'
                          "
                        />
                      </div>
                    </q-linear-progress>
                  </div>
                  <!-- <div
                    v-if="sortingType === 'fair'"
                    style="margin-top: 6px; margin-bottom: 6px"
                  >
                    Group satisfaction equality:&nbsp;&nbsp;&nbsp;
                    <q-rating
                      v-model="fairModel[JSON.parse(rest).id]"
                      size="1.5em"
                      :max="5"
                      color="orange"
                      icon-selected="img:https://img.icons8.com/material-rounded/24/FD7E14/anime-emoji--v1.png"
                      icon="img:https://img.icons8.com/ios/100/FD7E14/anime-emoji--v1.png"
                      readonly
                    ></q-rating>
                  </div> -->
                  <div
                    v-if="sortingType === 'attrfair'"
                    style="margin-top: 6px; margin-bottom: 6px"
                  >
                    Fairness and attractiveness score:
                    <q-linear-progress
                      :value="fair_attract[JSON.parse(rest).id]"
                      color="orange"
                      class="q-mt-sm"
                      size="18px"
                      style="width: 100%; border-radius: 15px"
                    >
                      <div class="absolute-full flex flex-center">
                        <q-badge
                          color="white"
                          text-color="accent"
                          :label="
                            parseInt(
                              parseFloat(
                                fair_attract[JSON.parse(rest).id]
                              ).toFixed(2) * 100
                            ) + '%'
                          "
                        />
                      </div>
                    </q-linear-progress>
                  </div>
                  <div
                    v-if="sortingType === 'sim'"
                    style="margin-top: 6px; margin-bottom: 6px"
                  >
                    Similarity to the group which bookmarked this
                    restaurant&nbsp;&nbsp;&nbsp;
                    <q-rating
                      v-model="similarityModel[JSON.parse(rest).id]"
                      size="1.2em"
                      :max="5"
                      icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                      icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                      readonly
                    ></q-rating>
                  </div>
                </q-card-section>
              </q-card-section>

              <q-card-section style="padding: 6px">
                <div
                  v-if="
                    extractDissatisfiedsBinary(JSON.parse(rest).id) &&
                    restaurantJsonRel.length > 0
                  "
                  style="
                    text-align: justify;
                    margin-bottom: 0px;
                    border-width: thin;
                    border-color: red;
                  "
                >
                  <q-separator style="margin-top: 6px" />

                  <q-list dense>
                    <q-item style="padding-left: 8px; padding-right: 8px" dense>
                      <q-item-section avatar dense style="padding-right: 0px">
                        <q-icon name="warning" color="amber-14" size="xs" />
                      </q-item-section>
                      <q-item-section
                        style="margin-left: -20px; padding-right: 0px"
                        dense
                      >
                        {{ sadsList[JSON.parse(rest).id] }}
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <div>
                    <q-list dense v-if="tripScore[JSON.parse(rest).id] >= 4">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant Quality
                        </q-item-section>
                      </q-item>
                    </q-list>

                    <q-list dense v-else>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-if="Boolean(JSON.parse(rest).price_eco)">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="attach_money" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are economic
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-if="Boolean(JSON.parse(rest).price_mid)">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon
                            name="attach_money"
                            color="yellow"
                            size="xs"
                          />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are mid-range
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list
                      dense
                      v-if="Boolean(JSON.parse(rest).price_expensive)"
                    >
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="attach_money" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are expensive
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-if="
                          (menuSizeRest[JSON.parse(rest).id]['category'] / 10) *
                            5 >
                          3.5
                        "
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Food category diversity
                        </q-item-section>
                      </q-item>

                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-else
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Food category diversity
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-if="popularityModel[JSON.parse(rest).id] >= 2.5"
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Popularity in this app
                        </q-item-section>
                      </q-item>
                      <q-item
                        v-else
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        ><q-item-section
                          avatar
                          dense
                          style="padding-right: 0px"
                        >
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Popularity in this app
                        </q-item-section></q-item
                      >
                    </q-list>
                  </div>
                </div>
                <div
                  v-if="
                    !extractDissatisfiedsBinary(JSON.parse(rest).id) &&
                    restaurantJsonRelActive
                  "
                  style="
                    text-align: justify;
                    margin-bottom: 0px;
                    border-width: thin;
                    border-color: green;
                  "
                >
                  <q-separator />
                  <div>
                    <q-list dense v-if="tripScore[JSON.parse(rest).id] >= 4">
                      <q-item
                        style="padding-left: 0px; padding-right: 0px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="offline_pin" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          High Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                  <q-list>
                    <q-item style="padding-left: 8px; padding-right: 8px" dense>
                      <q-item-section avatar dense>
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        style="margin-left: -20px; padding-right: 0px"
                        >All members will be satisfied with this restaurant.
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <q-list dense>
                    <q-item
                      style="padding-left: 0px; padding-right: 0px"
                      dense
                      v-if="
                        (menuSizeRest[JSON.parse(rest).id]['category'] / 10) *
                          5 >
                        4
                      "
                    >
                      <q-item-section avatar dense style="padding-right: 0px">
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        Food category diversity
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        <span
                          style="visibility: hidden; width: 0px; height: 0px"
                          >{{
                            (dishrelevancy =
                              (menuSizeRest[JSON.parse(rest).id]["category"] /
                                10) *
                              5)
                          }}</span
                        >
                        <!-- Update if the number of categories changes -->
                        <q-rating
                          v-model="dishrelevancy"
                          size="1.5em"
                          :max="5"
                          color="secondary"
                          readonly
                          icon="star_border"
                          icon-selected="star"
                          icon-half="star_half"
                          no-dimming
                        ></q-rating>
                      </q-item-section>
                    </q-item>
                    <q-item
                      style="padding-left: 0px; padding-right: 0px"
                      dense
                      v-if="
                        (menuSizeRest[JSON.parse(rest).id]['category'] / 10) *
                          5 >
                        3
                      "
                    >
                      <q-item-section avatar dense style="padding-right: 0px">
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        Food category diversity
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        <span
                          style="visibility: hidden; width: 0px; height: 0px"
                          >{{
                            (dishrelevancy =
                              (menuSizeRest[JSON.parse(rest).id]["category"] /
                                10) *
                              5)
                          }}</span
                        >
                        <!-- Update if the number of categories changes -->
                        <q-rating
                          v-model="dishrelevancy"
                          size="1.5em"
                          :max="5"
                          color="secondary"
                          readonly
                          icon="star_border"
                          icon-selected="star"
                          icon-half="star_half"
                          no-dimming
                        ></q-rating>
                      </q-item-section>
                    </q-item>
                    <q-item
                      style="padding-left: 0px; padding-right: 0px"
                      dense
                      v-if="
                        (menuSizeRest[JSON.parse(rest).id]['category'] / 10) *
                          5 >
                        0
                      "
                    >
                      <q-item-section avatar dense style="padding-right: 0px">
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        Food category diversity
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        <span
                          style="visibility: hidden; width: 0px; height: 0px"
                          >{{
                            (dishrelevancy =
                              (menuSizeRest[JSON.parse(rest).id]["category"] /
                                10) *
                              5)
                          }}</span
                        >
                        <!-- Update if the number of categories changes -->
                        <q-rating
                          v-model="dishrelevancy"
                          size="1.5em"
                          :max="5"
                          color="secondary"
                          readonly
                          icon="star_border"
                          icon-selected="star"
                          icon-half="star_half"
                          no-dimming
                        ></q-rating>
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <div>
                    <q-list dense v-if="tripScore[JSON.parse(rest).id] >= 4">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="offline_pin" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          High Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
          <div
            v-else
            class="q-pa-md row items-start q-gutter-md"
            style="
              margin-left: 2px auto;
              margin-right: 2px auto;
              margin-bottom: 7px auto;
              padding: 2px 2px 2px 2px;
            "
            :id="JSON.parse(rest).id"
          >
            <q-card class="my-card sadnessNotActive" flat bordered>
              <q-card-section horizontal style="cursor: pointer">
                <q-img
                  class="col-5"
                  :src="getLogo(JSON.parse(rest).logo)"
                  style="
                    padding: 2px;
                    width: 120px;
                    height: 120px;
                    cursor: pointer;
                  "
                  @click="goToRestPage(rest)"
                />
                <div
                  class="absolute"
                  style="top: 4px; left: 4px; border-radius: 25px"
                >
                  <div class="q-pa-md parent" style="padding: 5px">
                    <div class="q-gutter-y-md column">
                      <q-rating
                        v-model="model3[JSON.parse(rest).id]"
                        max="1"
                        size="25px"
                        color="red-14"
                        color-selected="red-9"
                        icon="favorite_border"
                        icon-selected="favorite"
                        @click="submitRemoveBookmark(JSON.parse(rest).id)"
                        style="background: LavenderBlush; border-radius: 8px"
                      />
                    </div>
                  </div>
                </div>
                <q-card-section
                  style="padding: 5px; width: 100%"
                  @click="goToRestPage(rest)"
                >
                  <q-list dense>
                    <q-item
                      dense
                      style="
                        margin-top: 0px;
                        margin-bottom: 0px;
                        margin-left: 0px;
                        padding: 0px 0px 0px 0px;
                      "
                    >
                      <q-item-section
                        dense
                        style="
                          margin-top: 0px;
                          margin-bottom: 0px;
                          margin-left: 0px;
                          padding: 0px 0px 0px 0px;
                        "
                      >
                        <strong>{{ JSON.parse(rest).name }}</strong>
                      </q-item-section>
                    </q-item>
                    <q-item
                      dense
                      style="
                        margin-top: 0px;
                        margin-bottom: 0px;
                        margin-left: 0px;
                        padding: 0px 0px 0px 0px;
                      "
                      ><q-item-section>{{
                        JSON.parse(rest).address
                      }}</q-item-section></q-item
                    >
                  </q-list>
                  <div v-if="sortingType === 'pop'">
                    <q-list dense>
                      <q-item
                        dense
                        style="
                          margin-top: 0px;
                          margin-bottom: 0px;
                          margin-left: 0px;
                          padding: 0px 0px 0px 0px;
                        "
                      >
                        <q-item-section
                          dense
                          style="
                            margin-top: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            padding: 0px 0px 0px 0px;
                          "
                        >
                          Popularity
                        </q-item-section>
                        <q-item-section dense>
                          <q-rating
                            v-model="popularityModel[JSON.parse(rest).id]"
                            max="5"
                            size="1.2em"
                            color="red"
                            color-selected="red-9"
                            icon="favorite_border"
                            icon-selected="favorite"
                            icon-half="favorite"
                            no-dimming
                            readonly
                          />
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <!-- <q-linear-progress
                      :value="
                        parseInt(popPercentage(JSON.parse(rest).id)) / 100
                      "
                      size="18px"
                      color="teal-3"
                      class="q-mt-sm"
                      style="width: 100%; border-radius: 15px"
                    >
                      <div class="absolute-full flex flex-center">
                        <q-badge
                          color="white"
                          text-color="accent"
                          :label="popPercentage(JSON.parse(rest).id) + '%'"
                        />
                      </div>
                    </q-linear-progress> -->
                    <!-- {{ populairtyModelFunc(JSON.parse(rest).id) }} -->
                  </div>
                  <div v-if="sortingType === 'avrattr'">
                    <q-list dense>
                      <q-item
                        dense
                        style="
                          margin-top: 0px;
                          margin-bottom: 0px;
                          margin-left: 0px;
                          padding: 0px 0px 0px 0px;
                        "
                      >
                        <q-item-section
                          dense
                          style="
                            margin-top: 0px;
                            margin-bottom: 0px;
                            margin-left: 0px;
                            padding: 0px 0px 0px 0px;
                          "
                        >
                          Fitness for your group
                        </q-item-section>
                        <q-item-section dense>
                          <q-rating
                            v-model="avrAttractModel[JSON.parse(rest).id]"
                            size="1.2em"
                            :max="5"
                            color="green"
                            readonly
                            icon="star_border"
                            icon-selected="star"
                            icon-half="star_half"
                            no-dimming
                          ></q-rating>
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                  <div v-if="sortingType === 'attr'">
                    <p style="margin-top: 6px; margin-bottom: 6px">
                      Satisfaction level for
                      {{
                        groupInfo[sortUserId][1] === "Organizer"
                          ? " you"
                          : groupInfo[sortUserId][1]
                      }}:
                      <!-- <q-linear-progress
                      :value="attractiveness[sortUserId][JSON.parse(rest).id]"
                      :color="groupInfo[sortUserId][0]"
                      class="q-mt-sm"
                      size="18px"
                      style="width: 100%; border-radius: 15px"
                    >
                      <div class="absolute-full flex flex-center">
                        <q-badge
                          color="white"
                          text-color="accent"
                          :label="
                            parseInt(
                              parseFloat(
                                attractiveness[sortUserId][JSON.parse(rest).id]
                              ).toFixed(2) * 100
                            ) + '%'
                          "
                        />
                      </div>
                    </q-linear-progress> -->
                    </p>
                  </div>

                  <!-- <div v-if="sortingType === 'fair'">
                    <p style="margin-top: 6px; margin-bottom: 6px">
                      Group satisfaction equality:&nbsp;&nbsp;&nbsp;

                      <q-rating
                        v-model="fairModel[JSON.parse(rest).id]"
                        size="1.5em"
                        :max="5"
                        color="orange"
                        icon-selected="img:https://img.icons8.com/material-rounded/24/FD7E14/anime-emoji--v1.png"
                        icon="img:https://img.icons8.com/ios/100/FD7E14/anime-emoji--v1.png"
                        readonly
                      ></q-rating>
                    </p>

                    <p></p>
                  </div> -->

                  <div v-if="sortingType === 'attrfair'">
                    Fairness and attractiveness score:
                    <!-- <q-linear-progress
                      :value="fair_attract[JSON.parse(rest).id]"
                      color="orange"
                      class="q-mt-sm"
                      size="18px"
                      style="width: 100%; border-radius: 15px"
                    >
                      <div class="absolute-full flex flex-center">
                        <q-badge
                          color="white"
                          text-color="accent"
                          :label="
                            parseInt(
                              parseFloat(
                                fair_attract[JSON.parse(rest).id]
                              ).toFixed(2) * 100
                            ) + '%'
                          "
                        />
                      </div>
                    </q-linear-progress> -->
                  </div>
                  <div v-if="sortingType === 'sim'">
                    <!-- {{ getSimilarity(JSON.parse(rest).id) }} -->
                    <!-- {{ similarityValue[JSON.parse(restPageInfo).id] }} -->
                    <p style="margin-top: 6px; margin-bottom: 6px">
                      Similarity to the group which bookmarked this
                      restaurant:&nbsp;&nbsp;&nbsp;
                      <!-- <q-linear-progress
                      :value="similarityValue[JSON.parse(rest).id]"
                      color="orange"
                      class="q-mt-sm"
                      size="18px"
                      style="width: 100%; border-radius: 15px"
                    >
                      <div class="absolute-full flex flex-center">
                        <q-badge
                          color="white"
                          text-color="accent"
                          :label="
                            parseInt(
                              similarityValue[JSON.parse(rest).id].toFixed(2) *
                                100
                            ) + '%'
                          "
                        />
                      </div>
                    </q-linear-progress> -->
                      <q-rating
                        v-model="similarityModel[JSON.parse(rest).id]"
                        size="1.2em"
                        :max="5"
                        icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                        icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                        readonly
                      ></q-rating>
                    </p>
                  </div>

                  <!--

                <div v-if="sortingType === 'attrfair'">
                  Fairness and attractiveness score:
                  <q-linear-progress
                    :value="fair_attract[JSON.parse(rest).id]"
                    color="orange"
                    class="q-mt-sm"
                  />
                </div>
                <div v-if="sortingType === 'sim'">
                  {{ getSimilarity(JSON.parse(rest).id) }}
                  Popularity in groups like yours:
                  <q-linear-progress
                    :value="similarityValue"
                    color="orange"
                    class="q-mt-sm"
                  />
                </div> -->
                </q-card-section>
              </q-card-section>
              <q-card-section style="padding: 6px">
                <div
                  v-if="
                    extractDissatisfiedsBinary(JSON.parse(rest).id) &&
                    restaurantJsonRel.length > 0
                  "
                  style="
                    text-align: justify;
                    margin-bottom: 0px;
                    border-width: thin;
                    border-color: red;
                  "
                >
                  <q-separator style="margin-top: 6px" />
                  <div>
                    <q-list dense v-if="tripScore[JSON.parse(rest).id] >= 4">
                      <q-item
                        style="padding-left: 0px; padding-right: 0px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="offline_pin" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          High Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </div>
                  <q-list dense>
                    <q-item style="padding-left: 0px; padding-right: 0px" dense>
                      <q-item-section
                        avatar
                        dense
                        style="padding-right: 0px; width: 16px"
                      >
                        <q-icon name="warning" color="amber-14" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <q-list dense v-if="tripScore[JSON.parse(rest).id] >= 4">
                    <q-item style="padding-left: 0px; padding-right: 0px" dense>
                      <q-item-section avatar dense>
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        TripAdvisor score
                      </q-item-section>
                      <q-item-section
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        <q-rating
                          v-model="tripScore[JSON.parse(rest).id]"
                          size="1.5em"
                          :max="5"
                          color="secondary"
                          readonly
                          icon="star_border"
                          icon-selected="star"
                          icon-half="star_half"
                          no-dimming
                        ></q-rating>
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <q-list
                    dense
                    v-if="popularityModel[JSON.parse(rest).id] >= 2.5"
                  >
                    <q-item style="padding-left: 0px; padding-right: 0px" dense>
                      <q-item-section avatar dense>
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        Popularity in this app
                      </q-item-section>
                      <q-item-section
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        <q-rating
                          v-model="popularityModel[JSON.parse(rest).id]"
                          max="5"
                          size="1.5em"
                          color="red"
                          color-selected="red-9"
                          icon="favorite_border"
                          icon-selected="favorite"
                          icon-half="favorite"
                          no-dimming
                          readonly
                        ></q-rating>
                      </q-item-section>
                    </q-item>
                  </q-list>

                  <q-list dense>
                    <q-item
                      style="padding-left: 0px; padding-right: 0px"
                      dense
                      v-if="
                        (menuSizeRest[JSON.parse(rest).id]['category'] / 10) *
                          5 >
                        3
                      "
                    >
                      <q-item-section avatar dense style="padding-right: 0px">
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        Food category diversity
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        <span
                          style="visibility: hidden; width: 0px; height: 0px"
                          >{{
                            (dishrelevancy =
                              (menuSizeRest[JSON.parse(rest).id]["category"] /
                                10) *
                              5)
                          }}</span
                        >
                        <!-- Update if the number of categories changes -->
                        <q-rating
                          v-model="dishrelevancy"
                          size="1.5em"
                          :max="5"
                          color="secondary"
                          readonly
                          icon="star_border"
                          icon-selected="star"
                          icon-half="star_half"
                          no-dimming
                        ></q-rating>
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <q-list dense>
                    <q-item
                      style="padding-left: 0px; padding-right: 0px"
                      dense
                      v-if="
                        (menuSizeRest[JSON.parse(rest).id]['dishes'] / 100) *
                          5 >
                        3
                      "
                    >
                      <q-item-section avatar dense style="padding-right: 0px">
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        Dish diversity
                      </q-item-section>
                      <q-item-section
                        dense
                        style="margin-left: -20px; padding-right: 0px"
                      >
                        <span
                          style="visibility: hidden; width: 0px; height: 0px"
                          >{{
                            (dishrelevancy =
                              (menuSizeRest[JSON.parse(rest).id]["dishes"] /
                                100) *
                              5)
                          }}</span
                        >
                        <q-rating
                          v-model="dishrelevancy"
                          size="1.5em"
                          :max="5"
                          color="secondary"
                          readonly
                          icon="star_border"
                          icon-selected="star"
                          icon-half="star_half"
                          no-dimming
                        ></q-rating>
                      </q-item-section>
                    </q-item>
                  </q-list>
                </div>

                <div
                  v-if="
                    !extractDissatisfiedsBinary(JSON.parse(rest).id) &&
                    restaurantJsonRelActive
                  "
                  style="
                    text-align: justify;
                    margin-bottom: 0px;
                    border-width: thin;
                    border-color: green;
                  "
                >
                  <!-- At least one of you will not be satisfied with this
                    restaurant. -->
                  <q-separator />
                  <q-list>
                    <q-item style="padding-left: 8px; padding-right: 8px" dense>
                      <q-item-section avatar dense>
                        <q-icon name="offline_pin" color="green" size="xs" />
                      </q-item-section>
                      <q-item-section
                        style="margin-left: -20px; padding-right: 0px"
                        >All members will be satisfied with this restaurant.
                      </q-item-section>
                    </q-item>
                  </q-list>
                  <div>
                    <q-list dense v-if="tripScore[JSON.parse(rest).id] >= 4">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-else>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-if="Boolean(JSON.parse(rest).price_eco)">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="attach_money" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are economic
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-if="Boolean(JSON.parse(rest).price_mid)">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon
                            name="attach_money"
                            color="yellow"
                            size="xs"
                          />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are mid-range
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list
                      dense
                      v-if="Boolean(JSON.parse(rest).price_expensive)"
                    >
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="attach_money" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are expensive
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-if="
                          (menuSizeRest[JSON.parse(rest).id]['category'] / 10) *
                            5 >
                          3.5
                        "
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Food category diversity
                        </q-item-section>
                      </q-item>

                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-else
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Food category diversity
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-if="popularityModel[JSON.parse(rest).id] >= 2.5"
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Popularity in this app
                        </q-item-section>
                      </q-item>
                      <q-item
                        v-else
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        ><q-item-section
                          avatar
                          dense
                          style="padding-right: 0px"
                        >
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Popularity in this app
                        </q-item-section></q-item
                      >
                    </q-list>
                  </div>
                </div>
                <div v-if="sortingType === 'pop' && !restaurantJsonRelActive">
                  <q-separator />
                  <div>
                    <q-list>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="help" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          style="margin-left: -20px; padding-right: 0px"
                          >Group members or preferences have not been added yet.
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-if="tripScore[JSON.parse(rest).id] >= 4">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-else>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant Quality
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-if="Boolean(JSON.parse(rest).price_eco)">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="attach_money" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are economic
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list dense v-if="Boolean(JSON.parse(rest).price_mid)">
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon
                            name="attach_money"
                            color="yellow"
                            size="xs"
                          />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are mid-range
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list
                      dense
                      v-if="Boolean(JSON.parse(rest).price_expensive)"
                    >
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                      >
                        <q-item-section avatar dense>
                          <q-icon name="attach_money" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Restaurant prices are expensive
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-if="
                          (menuSizeRest[JSON.parse(rest).id]['category'] / 10) *
                            5 >
                          3.5
                        "
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Food category diversity
                        </q-item-section>
                      </q-item>

                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-else
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Food category diversity
                        </q-item-section>
                      </q-item>
                    </q-list>
                    <q-list>
                      <q-item
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        v-if="popularityModel[JSON.parse(rest).id] >= 2.5"
                      >
                        <q-item-section avatar dense style="padding-right: 0px">
                          <q-icon name="thumb_up" color="green" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Popularity in this app
                        </q-item-section>
                      </q-item>
                      <q-item
                        v-else
                        style="padding-left: 8px; padding-right: 8px"
                        dense
                        ><q-item-section
                          avatar
                          dense
                          style="padding-right: 0px"
                        >
                          <q-icon name="thumb_down_alt" color="red" size="xs" />
                        </q-item-section>
                        <q-item-section
                          dense
                          style="margin-left: -20px; padding-right: 0px"
                        >
                          Popularity in this app
                        </q-item-section></q-item
                      >
                    </q-list>
                  </div>
                </div>
              </q-card-section>
            </q-card>
          </div>
        </div>
        <div class="centering"></div>
        <div
          v-if="
            relActive &&
            pageload &&
            pageloadbooked &&
            popularityModelLoad &&
            similarityValidity &&
            menuSizeValidity
          "
        >
          <div :class="{ clear: !relActive }">
            <!-- <q-page-scroller
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
            </q-page-scroller> -->
            <!-- <div v-if="RecomActive">
            <div>
              <div v-for="(rest, index) in restaurantJsonRel" :key="index">
                <div
                  class="q-pa-md row items-start q-gutter-md"
                  style="margin: 2px auto"
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
                    <q-card-section
                      class="q-pt-none"
                      @click="goToRestPage(rest)"
                    >
                      Address: {{ JSON.parse(rest).address }},
                      {{ JSON.parse(rest).city }}, Italy
                    </q-card-section>
                  </q-card>
                </div>
              </div>
            </div>
          </div> -->
          </div>
        </div>

        <!-- <div class="footer">
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
      </div> -->
      </div>
      <div
        v-if="
          restPageActive && pageload && pageloadbooked && popularityModelLoad
        "
      >
        {{ scrollToTop() }}
        <div
          style="
            position: fixed;
            z-index: 30;
            width: 100%;
            background-color: white;
            border-bottom: 1px solid;
            border-color: grey;
            padding-bottom: 6px;
            padding-top: 6px;
            display: inline-block;
            max-width: 600px;
            width: 100%;
            display: block;
            margin-left: auto;
            margin-right: auto;
          "
        >
          <div>
            <div>
              <q-icon
                size="xs"
                name="arrow_back_ios"
                color="primary"
                style="
                  margin-left: 20px;
                  margin-top: 2px;
                  float: left;
                  position: absolute;
                  cursor: pointer;
                "
                @click="scrollToAnchorPoint(JSON.parse(restPageInfo).id)"
              />
            </div>
            <div class="parent">
              <strong>{{ JSON.parse(restPageInfo).name }}</strong>
            </div>
          </div>
        </div>
        <!-- <q-btn
          round
          color="primary"
          icon="chevron_left"
          position="top-left"
          @click="scrollToAnchorPoint(JSON.parse(restPageInfo).id)"
          size="0.7em"
          class="button-back"
        /> -->
        <div
          class="card-position q-pa-md row items-start q-gutter-md"
          style="margin: 0px auto; padding-left: 2px; padding-right: 2px"
        >
          <q-card
            class="my-card"
            style="width: 100%; margin: auto; margin-top: 39px"
          >
            <img
              :src="getLogo(JSON.parse(restPageInfo).logo)"
              style="height: 200px; padding: 2px; border-radius: 5px"
            />
            <div
              class="absolute"
              style="top: 4px; left: 4px; border-radius: 25px"
            >
              <div class="q-pa-md" style="padding: 5px">
                <div class="q-gutter-y-md column">
                  <q-rating
                    v-model="model3[JSON.parse(restPageInfo).id]"
                    max="1"
                    size="25px"
                    color="red-14"
                    color-selected="red-9"
                    icon="favorite_border"
                    icon-selected="favorite"
                    @click="submitRemoveBookmark(JSON.parse(restPageInfo).id)"
                    style="background: LavenderBlush; border-radius: 8px"
                  />
                </div>
              </div>
            </div>
            <q-card-section
              class="q-pt-none"
              style="
                width: 100%;
                max-width: 100%;
                padding-left: 1px;
                padding-right: 1px;
                padding-top: 1px;
                padding-bottom: 1px;
              "
            >
              <div
                class="q-pa-md row items-start q-gutter-md"
                style="width: 100%; padding-right: 0px"
              >
                <q-card class="my-card" style="width: 100%">
                  <q-card-section>
                    <div class="card-styling">
                      <div class="text-h6 q-mb-xs">
                        {{ JSON.parse(restPageInfo).name }}
                      </div>
                      <p
                        style="
                          text-align: justify;
                          text-justify: inter-word;
                          padding-bottom: 2px;
                          margin-bottom: 0px;
                        "
                      >
                        {{ JSON.parse(restPageInfo).address }}
                      </p>
                      <p style="padding-bottom: 2px; margin-bottom: 0px">
                        <a
                          :href="links[JSON.parse(restPageInfo).name]"
                          style="text-decoration: none"
                          target="_blank"
                          ><b>Restaurant Page</b></a
                        >
                      </p>

                      <div
                        v-if="
                          extractDissatisfiedsBinary(
                            JSON.parse(restPageInfo).id
                          ) && restaurantJsonRel.length > 0
                        "
                        style="
                          text-align: justify;
                          margin-bottom: 0px;
                          border-width: thin;
                          border-color: red;
                        "
                      >
                        <q-separator style="margin-top: 6px" />

                        <q-list dense>
                          <q-item
                            style="padding-left: 0px; padding-right: 8px"
                            dense
                          >
                            <q-item-section
                              avatar
                              dense
                              style="padding-right: 0px"
                            >
                              <q-icon
                                name="warning"
                                color="amber-14"
                                size="x"
                              />
                            </q-item-section>
                            <q-item-section
                              style="margin-left: -16px; padding-right: 0px"
                              dense
                            >
                              {{ sadsList[JSON.parse(restPageInfo).id] }}
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                      <div v-else>
                        <q-list>
                          <q-item
                            style="padding-left: 0px; padding-right: 8px"
                            dense
                          >
                            <q-item-section avatar dense>
                              <q-icon
                                name="offline_pin"
                                color="green"
                                size="x"
                              />
                            </q-item-section>
                            <q-item-section
                              style="margin-left: -16px; padding-right: 0px"
                              >All members will be satisfied with this
                              restaurant.
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>

                      <q-separator
                        style="margin-top: 2px; margin-bottom: 2px"
                      />
                      <div
                        class="q-pa-md"
                        style="
                          width: 100%;
                          padding-top: 0px;
                          padding-right: 0px;
                          padding-left: 0px;
                          padding-bottom: 0px;
                        "
                      >
                        <q-list class="rounded-borders">
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
                                :label="
                                  food_name_change(category) +
                                  ' (' +
                                  String(foodList.length) +
                                  ')'
                                "
                              >
                                <div
                                  class="q-pa-md"
                                  style="width: 100%; padding-top: 0px"
                                >
                                  <div
                                    v-for="(food, indexIn) in foodList"
                                    :key="indexIn"
                                  >
                                    <q-list>
                                      <q-item clickable v-ripple>
                                        <q-item-section
                                          style="margin-left: 60px"
                                          >{{ food }}</q-item-section
                                        >
                                      </q-item>
                                    </q-list>
                                    <q-separator
                                      style="
                                        margin-top: 2px;
                                        margin-bottom: 2px;
                                      "
                                    />
                                  </div>
                                </div>
                              </q-expansion-item>
                            </div>
                          </q-expansion-item>
                        </q-list>
                      </div>
                      <q-separator style="margin-bottom: 10px" />
                      <p
                        v-show="Boolean(JSON.parse(restPageInfo).price_eco)"
                        style="
                          margin-bottom: 8px;
                          text-align: justify;
                          text-justify: inter-word;
                        "
                      >
                        Restaurant price is <strong>economic</strong>. Do you
                        prefer to change the price range to mid-range or
                        expensive?
                      </p>
                      <div
                        class="parent"
                        v-show="Boolean(JSON.parse(restPageInfo).price_eco)"
                      >
                        <q-btn
                          icon="price_change"
                          color="primary"
                          label="Mid-range"
                          @click="price('mid')"
                          class="critique-btn"
                        />
                        <q-btn
                          icon="price_change"
                          color="primary"
                          label="Expensive"
                          @click="price('exp')"
                          class="critique-btn"
                        />
                      </div>
                      <p
                        v-show="Boolean(JSON.parse(restPageInfo).price_mid)"
                        style="
                          margin-bottom: 8px;
                          text-align: justify;
                          text-justify: inter-word;
                        "
                      >
                        Restaurant price is <strong>mid-range</strong>. Do you
                        prefer to change the price range to economical or
                        expensive?
                      </p>
                      <div
                        class="parent"
                        v-show="Boolean(JSON.parse(restPageInfo).price_mid)"
                      >
                        <q-btn
                          color="primary"
                          icon="price_change"
                          label="Economic"
                          @click="price('eco')"
                          class="critique-btn"
                        />
                        <q-btn
                          color="primary"
                          icon="price_change"
                          label="Expensive"
                          @click="price('exp')"
                          class="critique-btn"
                        />
                      </div>
                      <p
                        v-show="
                          Boolean(JSON.parse(restPageInfo).price_expensive)
                        "
                        style="
                          margin-bottom: 8px;
                          text-align: justify;
                          text-justify: inter-word;
                        "
                      >
                        Restaurant price is <strong>expensive</strong>. Do you
                        prefer to change the price range to economical or
                        mid-range?
                      </p>
                      <div
                        class="parent"
                        v-show="
                          Boolean(JSON.parse(restPageInfo).price_expensive)
                        "
                      >
                        <q-btn
                          color="primary"
                          icon="price_change"
                          label="Economic"
                          @click="price('eco')"
                          class="critique-btn"
                        />
                        <q-btn
                          color="primary"
                          icon="price_change"
                          label="Mid-range"
                          @click="price('mid')"
                          class="critique-btn"
                        />
                      </div>
                    </div>
                    <q-separator style="margin-bottom: 2px; margin-top: 10px" />
                    <div class="card-styling">
                      <!-- <div
                        v-if="sortingType === 'pop'"
                        style="
                          display: inline;
                          width: 100%;
                          margin-bottom: 8px;
                          padding-bottom: 4px;
                        "
                      > -->
                      <!-- <div>
                          Popularity in this app
                          <q-icon
                            size="xxs"
                            name="info"
                            color="primary"
                            @click="scoreDialogFunc('pop')"
                          />
                          <q-linear-progress
                            :value="
                              parseInt(
                                popPercentage(JSON.parse(restPageInfo).id)
                              ) / 100
                            "
                            size="18px"
                            color="teal-3"
                            class="q-mt-sm"
                            style="width: 100%; border-radius: 15px"
                          >
                            <div class="absolute-full flex flex-center">
                              <q-badge
                                color="white"
                                text-color="accent"
                                :label="
                                  popPercentage(JSON.parse(restPageInfo).id) +
                                  '%'
                                "
                              />
                            </div>
                          </q-linear-progress>
                        </div> -->
                      <!-- <p style="margin-top: 6px; margin-bottom: 6px">
                          Popularity<q-icon
                            size="xxs"
                            name="info"
                            color="primary"
                            @click="scoreDialogFunc('pop')"
                          />:&nbsp;&nbsp;&nbsp;
                          <q-rating
                            v-model="
                              popularityModel[JSON.parse(restPageInfo).id]
                            "
                            max="5"
                            size="1.5em"
                            color="red"
                            color-selected="red-9"
                            icon="favorite_border"
                            icon-selected="favorite"
                            icon-half="favorite"
                            no-dimming
                            readonly
                          />
                        </p>
                      </div> -->
                      <!-- <div v-if="sortingType === 'avrattr'">
                        <p style="margin-top: 6px; margin-bottom: 6px">
                          Fitness for your group:
                          <q-icon
                            size="xxs"
                            name="info"
                            color="primary"
                            @click="scoreDialogFunc('avrattr')"
                          />: &nbsp;&nbsp;&nbsp; -->
                      <!-- <q-linear-progress
                          :value="avrAttract[JSON.parse(restPageInfo).id]"
                          color="orange"
                          class="q-mt-sm"
                          size="18px"
                          style="width: 100%; border-radius: 15px"
                        >
                          <div class="absolute-full flex flex-center">
                            <q-badge
                              color="white"
                              text-color="accent"
                              :label="
                                parseInt(
                                  parseFloat(
                                    avrAttract[JSON.parse(restPageInfo).id]
                                  ).toFixed(2) * 100
                                ) + '%'
                              "
                            />
                          </div>
                        </q-linear-progress> -->
                      <!-- <q-rating
                            v-model="
                              avrAttractModel[JSON.parse(restPageInfo).id]
                            "
                            size="1.5em"
                            :max="5"
                            color="orange"
                            readonly
                            icon="star_border"
                            icon-selected="star"
                            icon-half="star_half"
                          ></q-rating>
                        </p>
                      </div> -->

                      <!-- <div v-if="sortingType === 'attr'">
                        Satisfaction level for
                        {{
                          groupInfo[sortUserId][1] === "Organizer"
                            ? " you"
                            : groupInfo[sortUserId][1]
                        }}
                        <q-icon
                          size="xxs"
                          name="info"
                          color="primary"
                          @click="scoreDialogFunc('attr')"
                        />
                        <q-linear-progress
                          :value="
                            attractiveness[sortUserId][
                              JSON.parse(restPageInfo).id
                            ]
                          "
                          :color="groupInfo[sortUserId][0]"
                          class="q-mt-sm"
                          size="18px"
                          style="width: 100%; border-radius: 15px"
                        >
                          <div class="absolute-full flex flex-center">
                            <q-badge
                              color="white"
                              text-color="accent"
                              :label="
                                parseInt(
                                  parseFloat(
                                    attractiveness[sortUserId][
                                      JSON.parse(restPageInfo).id
                                    ]
                                  ).toFixed(2) * 100
                                ) + '%'
                              "
                            />
                          </div>
                        </q-linear-progress>
                      </div> -->
                      <!-- <div v-if="sortingType === 'fair'">
                        <p style="margin-top: 6px; margin-bottom: 6px">
                          Group satisfaction equality
                          <q-icon
                            size="xxs"
                            name="info"
                            color="primary"
                            @click="
                              scoreDialogFunc(
                                'fair',
                                JSON.parse(restPageInfo).id
                              )
                            "
                          />:&nbsp;&nbsp;&nbsp; -->
                      <!-- <q-linear-progress
                          :value="fariness(JSON.parse(restPageInfo).id)"
                          color="orange"
                          class="q-mt-sm"
                          size="18px"
                          style="width: 100%; border-radius: 15px"
                        >
                          <div class="absolute-full flex flex-center">
                            <q-badge
                              color="white"
                              text-color="accent"
                              :label="
                                parseInt(
                                  parseFloat(
                                    fariness(JSON.parse(restPageInfo).id)
                                  ).toFixed(2) * 100
                                ) + '%'
                              "
                            />
                          </div>
                        </q-linear-progress> -->
                      <!-- <q-rating
                            v-model="fairModel[JSON.parse(restPageInfo).id]"
                            size="1.5em"
                            :max="5"
                            color="orange"
                            icon-selected="img:https://img.icons8.com/material-rounded/24/FD7E14/anime-emoji--v1.png"
                            icon="img:https://img.icons8.com/ios/100/FD7E14/anime-emoji--v1.png"
                            readonly
                          ></q-rating>
                        </p>
                      </div> -->

                      <!-- <div v-if="sortingType === 'attrfair'">
                        Fairness and attractiveness score
                        <q-icon
                          size="xxs"
                          name="info"
                          color="primary"
                          @click="scoreDialogFunc('attrfair')"
                        />
                        <q-linear-progress
                          :value="fair_attract[JSON.parse(restPageInfo).id]"
                          color="orange"
                          class="q-mt-sm"
                          size="18px"
                          style="width: 100%; border-radius: 15px"
                        >
                          <div class="absolute-full flex flex-center">
                            <q-badge
                              color="white"
                              text-color="accent"
                              :label="
                                parseInt(
                                  parseFloat(
                                    fair_attract[JSON.parse(restPageInfo).id]
                                  ).toFixed(2) * 100
                                ) + '%'
                              "
                            />
                          </div>
                        </q-linear-progress>
                      </div> -->
                      <!-- <div v-if="sortingType === 'sim'">
                        <p style="margin-top: 6px; margin-bottom: 6px"> -->
                      <!-- {{ getSimilarity(JSON.parse(rest).id) }} -->
                      <!-- {{ similarityValue[JSON.parse(restPageInfo).id] }} -->
                      <!-- Similarity to groups who liked this restaurant
                          <q-icon
                            size="xxs"
                            name="info"
                            color="primary"
                            @click="scoreDialogFunc('sim')"
                          />:&nbsp;&nbsp;&nbsp; -->
                      <!-- <q-linear-progress
                          :value="similarityValue[JSON.parse(restPageInfo).id]"
                          color="orange"
                          class="q-mt-sm"
                          size="18px"
                          style="width: 100%; border-radius: 15px"
                        >
                          <div class="absolute-full flex flex-center">
                            <q-badge
                              color="white"
                              text-color="accent"
                              :label="
                                parseInt(
                                  similarityValue[
                                    JSON.parse(restPageInfo).id
                                  ].toFixed(2) * 100
                                ) + '%'
                              "
                            />
                          </div>
                        </q-linear-progress> -->

                      <!-- <q-rating
                            v-model="
                              similarityModel[JSON.parse(restPageInfo).id]
                            "
                            size="1.5em"
                            :max="5"
                            icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                            icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                            readonly
                          ></q-rating>
                        </p>
                      </div> -->

                      <q-list class="rounded-borders">
                        <q-item @click="scoreDialogFunc('pop')">
                          <q-item-section>Popularity</q-item-section>
                          <q-item-section>
                            <q-rating
                              v-model="
                                popularityModel[JSON.parse(restPageInfo).id]
                              "
                              max="5"
                              size="1.5em"
                              color="red"
                              color-selected="red-9"
                              icon="favorite_border"
                              icon-selected="favorite"
                              icon-half="favorite"
                              no-dimming
                              readonly
                          /></q-item-section>
                          <q-item-section avatar
                            ><q-icon
                              size="sm"
                              name="info"
                              color="primary"
                              @click="scoreDialogFunc('pop')"
                              style="cursor: pointer"
                            /> </q-item-section
                        ></q-item>
                      </q-list>
                      <div v-if="restaurantJsonRelActive" class="card-styling">
                        <q-list class="rounded-borders">
                          <q-item @click="scoreDialogFunc('avrattr')">
                            <q-item-section
                              >Fitness for your group</q-item-section
                            >
                            <q-item-section>
                              <q-rating
                                v-model="
                                  avrAttractModel[JSON.parse(restPageInfo).id]
                                "
                                max="5"
                                size="1.5em"
                                color="green"
                                icon="star_border"
                                icon-selected="star"
                                icon-half="star_half"
                                no-dimming
                                readonly
                            /></q-item-section>
                            <q-item-section avatar
                              ><q-icon
                                size="sm"
                                name="info"
                                color="primary"
                                @click="scoreDialogFunc('avrattr')"
                                style="cursor: pointer"
                              /> </q-item-section
                          ></q-item>
                        </q-list>
                        <q-list class="rounded-borders">
                          <q-item
                            @click="
                              scoreDialogFunc(
                                'sim',
                                JSON.parse(restPageInfo).id
                              )
                            "
                          >
                            <q-item-section
                              >Similarity to the group which bookmarked this
                              restaurant</q-item-section
                            >
                            <q-item-section>
                              <q-rating
                                v-model="
                                  similarityModel[JSON.parse(restPageInfo).id]
                                "
                                size="1.5em"
                                :max="5"
                                icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                                icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                                readonly
                            /></q-item-section>
                            <q-item-section avatar
                              ><q-icon
                                size="sm"
                                name="info"
                                color="primary"
                                @click="
                                  scoreDialogFunc(
                                    'sim',
                                    JSON.parse(restPageInfo).id
                                  )
                                "
                                style="cursor: pointer"
                              /> </q-item-section
                          ></q-item>
                        </q-list>
                      </div>
                      <div
                        class="card-styling"
                        style="margin-top: 8px; margin-bottom: 16px"
                      >
                        <q-list dense class="rounded-borders">
                          <q-item dense>
                            <q-item-section dense>
                              TripAdvisor score
                            </q-item-section>
                            <q-item-section dense>
                              <q-rating
                                v-model="tripScore[JSON.parse(restPageInfo).id]"
                                size="1.5em"
                                :max="5"
                                color="secondary"
                                readonly
                                icon="star_border"
                                icon-selected="star"
                                icon-half="star_half"
                                no-dimming
                              ></q-rating> </q-item-section
                            ><q-item-section avatar
                              ><q-icon
                                size="sm"
                                name="info"
                                color="primary"
                                @click="
                                  scoreDialogFunc(
                                    'trip',
                                    JSON.parse(restPageInfo).id
                                  )
                                "
                                style="cursor: pointer"
                              />
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>

                      <div
                        class="card-styling"
                        style="margin-top: 8px; margin-bottom: 16px"
                      >
                        <q-list dense class="rounded-borders">
                          <q-item dense>
                            <q-item-section dense>
                              Food category diversity
                            </q-item-section>
                            <q-item-section dense>
                              <span
                                style="
                                  visibility: hidden;
                                  width: 0px;
                                  height: 0px;
                                "
                                >{{
                                  (dishrelevancy =
                                    (menuSizeRest[JSON.parse(restPageInfo).id][
                                      "category"
                                    ] /
                                      10) *
                                    5)
                                }}</span
                              >
                              <!-- Update if the number of categories changes -->
                              <q-rating
                                v-model="dishrelevancy"
                                size="1.5em"
                                :max="5"
                                color="secondary"
                                readonly
                                icon="star_border"
                                icon-selected="star"
                                icon-half="star_half"
                                no-dimming
                              ></q-rating> </q-item-section
                            ><q-item-section avatar
                              ><q-icon
                                size="sm"
                                name="info"
                                color="primary"
                                @click="scoreDialogFunc('categ')"
                                style="cursor: pointer"
                              />
                            </q-item-section> </q-item
                        ></q-list>
                      </div>
                      <div
                        class="card-styling"
                        style="margin-top: 8px; margin-bottom: 16px"
                      >
                        <q-list dense class="rounded-borders">
                          <q-item dense>
                            <q-item-section dense>
                              Dish diversity
                            </q-item-section>
                            <q-item-section dense>
                              <span
                                style="
                                  visibility: hidden;
                                  width: 0px;
                                  height: 0px;
                                "
                                >{{
                                  (dishrelevancy =
                                    (menuSizeRest[JSON.parse(restPageInfo).id][
                                      "dishes"
                                    ] /
                                      100) *
                                    5)
                                }}</span
                              >
                              <q-rating
                                v-model="dishrelevancy"
                                size="1.5em"
                                :max="5"
                                color="secondary"
                                readonly
                                icon="star_border"
                                icon-selected="star"
                                icon-half="star_half"
                                no-dimming
                              ></q-rating> </q-item-section
                            ><q-item-section avatar
                              ><q-icon
                                size="sm"
                                name="info"
                                color="primary"
                                @click="scoreDialogFunc('dishDiv')"
                                style="cursor: pointer"
                              />
                            </q-item-section>
                          </q-item>
                        </q-list>
                      </div>
                    </div>
                  </q-card-section>
                </q-card>
              </div>
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
            </q-card-section>

            <!-- <q-card-section style="padding-top: 0px"> </q-card-section> -->
          </q-card>
        </div>
      </div>
    </div>
    <div v-else style="height: 100vh">
      <div class="no-tasks absolute-center text-h5 text-primary text-center">
        <div class="q-pa-md flex flex-center">
          <q-circular-progress
            indeterminate
            size="50px"
            color="lime"
            class="q-ma-md"
          />
        </div>
      </div>
    </div>
  </div>
  <!-- <div v-else>
    <div class="no-tasks absolute-center text-h5 text-primary text-center">
      Thank you for participating in our user study. For starting a new session
      just click on the following button:
      <q-btn color="primary" style="opacity: 1" @click="newSessoin()"
        >New Session</q-btn
      >
    </div>
  </div> -->
</template>

<script>
import axios from "axios";
import { ref } from "vue";
export default {
  emits: ["goToGroupPage", "critiqueIssued", "activeRevision"],
  props: [
    "groupInfo",
    "groupId",
    "userPreferenceList",
    "critiqueRange",
    "currentRestaurant",
  ],
  data() {
    return {
      tripPage: {
        1: "www.tripadvisor.com/Restaurant_Review-g784829-d3454918-Reviews-Alpenrestaurant_Elisabeth-Sarentino_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        2: "https://www.tripadvisor.com/Hotel_Review-g2617727-d2621506-Reviews-Ansitz_Romani-Termeno_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        3: "https://www.tripadvisor.com/Restaurant_Review-g187857-d4909490-Reviews-Mister_Ye-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        4: "https://www.tripadvisor.de/Restaurant_Review-g2617727-d1177112-Reviews-Restaurant_Pizzeria_Burgerstube_Tramin-Termeno_Province_of_South_Tyrol_Trentino_.html",
        5: "https://www.tripadvisor.it/Restaurant_Review-g187857-d13223027-Reviews-Cibus-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        6: "https://www.tripadvisor.com/Restaurant_Review-g187857-d13163370-Reviews-Forst_Season-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        7: "https://www.tripadvisor.it/Restaurant_Review-g187857-d1056993-Reviews-Franziskanerstuben-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        8: "https://www.tripadvisor.de/Restaurant_Review-g187857-d1055405-Reviews-Gasthaus_Fink-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        9: "https://www.tripadvisor.it/Restaurant_Review-g187857-d1106537-Reviews-Walthers-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        10: "https://www.tripadvisor.it/ShowUserReviews-g6440469-d10090134-r826367996-Zunerhof-Longostagno_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        11: "https://www.tripadvisor.it/Restaurant_Review-g1436137-d1091575-Reviews-Zur_Rose-Appiano_sulla_Strada_del_Vino_Province_of_South_Tyrol_Trentino_Alto_Adi.html",
        12: "https://www.tripadvisor.it/Hotel_Review-g187857-d529789-Reviews-Gasthof_Kohlern-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        13: "https://www.tripadvisor.de/Hotel_Review-g1436137-d1915710-Reviews-Gasthof_zum_Guten_Tropfen-Appiano_sulla_Strada_del_Vino_Province_of_South_Tyrol_Trent.html",
        15: "https://www.tripadvisor.de/Hotel_Review-g612438-d8021501-Reviews-Gasthof_zur_Muhle-Ora_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        16: "https://www.tripadvisor.it/Restaurant_Review-g1436137-d3488406-Reviews-Hotel_Gasthof_Steinegge-Appiano_sulla_Strada_del_Vino_Province_of_South_Tyrol_Tr.html",
        17: "https://www.tripadvisor.com/Restaurant_Review-g187857-d1147770-Reviews-Pizzeria_Geier-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        18: "https://www.tripadvisor.com/Restaurant_Review-g670610-d16819722-Reviews-Gloriette_Guesthouse_Ristorantino_Lounge-Soprabolzano_Renon_Province_of_South_Ty.html",
        19: "https://www.tripadvisor.com/Restaurant_Review-g946905-d1091563-Reviews-Gretl_am_See-Caldaro_sulla_Strada_del_Vino_Province_of_South_Tyrol_Trentino_Alto_.html",
        20: "https://www.tripadvisor.com/Restaurant_Review-g187857-d20296337-Reviews-WineBistro_Gries_13-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        21: "https://www.tripadvisor.it/ShowUserReviews-g187857-d788203-r315259924-Hopfen_Co-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        22: "https://www.tripadvisor.com/Hotel_Review-g946905-d613048-Reviews-Hotel_Restaurant_Haus_am_Hang-Caldaro_sulla_Strada_del_Vino_Province_of_South_Tyrol_Tre.html",
        23: "https://www.tripadvisor.com/Restaurant_Review-g187857-d1137202-Reviews-Restaurant_Post_Gries-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        24: "https://www.tripadvisor.com/Restaurant_Review-g194876-d7142548-Reviews-Restaurant_Hotel_Lichtenstern-Renon_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        25: "https://www.tripadvisor.com/Restaurant_Review-g187857-d2535733-Reviews-Magdalener_Hof-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        26: "https://www.tripadvisor.com/Restaurant_Review-g1055435-d1073216-Reviews-Restaurant_Rotwand-Laives_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        27: "https://www.tripadvisor.com/Restaurant_Review-g187857-d9812955-Reviews-Ichiban-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        28: "https://www.tripadvisor.it/Restaurant_Review-g187857-d7256508-Reviews-Il_Corso_Pizzeria_Ristorante-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        29: "https://www.tripadvisor.com/Restaurant_Review-g187857-d1055116-Reviews-Imbiss_Kampill-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        30: "https://www.tripadvisor.it/Restaurant_Review-g187857-d12675413-Reviews-In_Viaggio_Claudio_Melis_Ristorante-Bolzano_Province_of_South_Tyrol_Trentino_Alt.html",
        31: "https://www.tripadvisor.it/Restaurant_Review-g187857-d10214354-Reviews-Koi-Bolzano_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
        32: "https://www.tripadvisor.it/Hotel_Review-g947873-d23646365-Reviews-Manna_Resort-Montagna_Province_of_South_Tyrol_Trentino_Alto_Adige.html",
      },
      tripScore: {
        1: 4,
        2: 4.5,
        3: 4,
        4: 4,
        5: 4,
        6: 4,
        7: 4.5,
        8: 3.5,
        9: 3,
        10: 4.5,
        11: 4.5,
        12: 4.5,
        13: 4.5,
        15: 4.5,
        16: 4.5,
        17: 4,
        18: 5,
        19: 4,
        20: 4,
        21: 2,
        22: 4.5,
        23: 4,
        24: 4.5,
        25: 4,
        26: 4.5,
        27: 3.5,
        28: 4.5,
        29: 3.5,
        30: 5,
        31: 4.5,
        32: 5,
      },
      revisionFlag: {},
      revisionFlagTemp: true,
      revisionTaggle: false,
      simRestExp: {},
      sadsList: {},
      countPopularity: {},
      attractivenessModel: {},
      fairModel: {},
      similarityModel: {},
      avrAttractModel: {},
      popularityModelLoad: false,
      popularityModel: {},
      bannerToggle: false,
      attractiveness: {},
      happyValidator: false,
      sadValidator: false,
      userAttractive: {},
      componentKey: ref(0),
      similarityValidity: true,
      modelGroup: ref(3.5),
      pageloadbooked: false,
      selectLoad: {},
      sortingType: "pop",
      sortUserId: -1,
      RecomActive: false,
      restaurantJsonRelActive: false,
      organizer_user_attractiveness: {},
      fair_attract: {},
      memberColordelete: ["blue", "green", "purple", "red", "yellow"],
      sortLabel: "Sort: By minimizing individual dissatisfaction",
      selectedPopularityObj: {},
      popularityObj: {},
      endOfSession: false,
      links: require(`../assets/external_link.json`),
      counterBtnRel: 0,
      counterBtn: 0,
      distanceAvr: 0,
      distanceCounter: 0,
      locationValidity: false,
      similarityValue: {},
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
      similarityExplanation: "",
      membersDistance: {},
      maxDistance: 0,
      restPageActive: false,
      maxpagePop: 1,
      maxpageRel: 1,
      pageload: false,
      restaurantJsonRel: {},
      bookmarked: [],
      model: ref(1),
      model3: {},
      subpage: "pop",
      popActive: false,
      relActive: true,
      restaurantJson: {},
      menuList: {},
      group_id_intract: JSON.parse(sessionStorage.getItem("group_id")),
      restaurantJsonRelOrignal: {},
      sortDialog: ref(false),
      priceDialog: ref(false),
      position: ref("bottom"),
      positionExplan: ref("bottom"),
      positionPrice: ref("bottom"),
      sortType: "",
      sortActive: "",
      individualExplanation: "",
      avrAttract: {},
      scoreDialog: ref(false),
      scoreExplanation: "",
      menuSizeRest: {},
      menuSizeValidity: false,
      icons: [
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
      ],
    };
  },
  methods: {
    getIndiExplanSim(indiId, name, restId) {
      var similarityExplanation = this.simRestExp[restId];
      var individualList = [];
      for (var tempList of this.userPreferenceList) {
        if (
          tempList[1] === indiId &&
          typeof similarityExplanation[tempList[0]] !== "undefined"
        ) {
          if (
            similarityExplanation[tempList[0]] /
              this.countPopularity[tempList[0]] >
            1
          ) {
            individualList.push(this.food_name_change(tempList[0]));
          }
        }
      }
      if (individualList.length === 0) {
        var explanation =
          "This restaurant is not very often chosen by groups that would like to eat ";
        explanation +=
          this.groupInfo[indiId][1] === "Organizer"
            ? "your"
            : this.groupInfo[indiId][1] + "'s";
        explanation += " favorit dishes.";
      } else {
        var explanation =
          "This restaurant is often chosen by groups that would like to eat ";
        explanation +=
          this.groupInfo[indiId][1] === "Organizer"
            ? "your"
            : this.groupInfo[indiId][1] + "'s";
        explanation += " favorit dishes, namely,";
        var counter = 0;
        for (var key of individualList) {
          counter++;
          explanation += " " + key;
          if (counter < individualList.length - 1) {
            explanation += ", ";
          } else if (counter === individualList.length - 1) {
            explanation += ", and ";
          } else {
            explanation += ".";
          }
        }
      }
      return explanation;
    },
    getIndiExplan(menuGet, indiId, gInfo, name, restIdExplain) {
      var menu = menuGet;
      const urlmnue =
        "http://46.18.25.97:8050/restaurant/menu/" + restIdExplain;
      axios.get(urlmnue).then((response) => {
        menu = JSON.parse(JSON.stringify(response.data));

        var individualList = {};
        for (var tempList of this.userPreferenceList) {
          if (tempList[1] === indiId && menu[tempList[0]].length > 0) {
            individualList[tempList[0]] = menu[tempList[0]].length;
          }
        }
        var explanation =
          this.groupInfo[indiId][1] === "Organizer"
            ? "you"
            : this.groupInfo[indiId][1];
        explanation =
          explanation.charAt(0).toUpperCase() + explanation.slice(1);
        explanation += " have ";
        if (Object.keys(individualList).length === 0) {
          explanation += "no choice.";
        } else {
          var counter = 0;
          for (var key of Object.keys(individualList)) {
            counter++;
            if (individualList[key] > 1) {
              explanation +=
                String(individualList[key]) +
                " kinds of " +
                this.food_name_change(String(key));
            } else {
              explanation +=
                String(individualList[key]) +
                " kind of " +
                this.food_name_change(String(key));
            }
            if (counter < Object.keys(individualList).length - 1) {
              explanation += ", ";
            } else if (counter === Object.keys(individualList).length - 1) {
              explanation += ", and ";
            } else {
              explanation += " to select from.";
            }
          }
        }
        this.individualExplanation = explanation;
        return explanation;
      });
    },
    fairnessIcon(rating) {
      if (rating <= 1) {
        this.icons = [
          "sentiment_very_dissatisfied",
          "sentiment_very_dissatisfied",
          "sentiment_very_dissatisfied",
          "sentiment_very_dissatisfied",
          "sentiment_very_dissatisfied",
        ];
      } else if (rating <= 2) {
        this.icons = [
          "sentiment_dissatisfied",
          "sentiment_dissatisfied",
          "sentiment_dissatisfied",
          "sentiment_dissatisfied",
          "sentiment_dissatisfied",
        ];
      } else if (rating <= 3) {
        this.icons = [
          "sentiment_neutral",
          "sentiment_neutral",
          "sentiment_neutral",
          "sentiment_neutral",
          "sentiment_neutral",
        ];
      } else if (rating <= 4) {
        this.icons = [
          "sentiment_satisfied",
          "sentiment_satisfied",
          "sentiment_satisfied",
          "sentiment_satisfied",
          "sentiment_satisfied",
        ];
      } else if (rating <= 5) {
        this.icons = [
          "sentiment_very_satisfied",
          "sentiment_very_satisfied",
          "sentiment_very_satisfied",
          "sentiment_very_satisfied",
          "sentiment_very_satisfied",
        ];
      }
    },
    bannerToggler() {
      this.bannerToggle = false;
    },
    RevisionBannerTogglerCancel() {
      this.revisionTaggle = false;
    },
    revisionflagToggler(id, validation) {
      if (this.revisionFlag[id] === undefined) {
        if (
          validation &&
          this.revisionFlagTemp &&
          this.revisionFlag[id] === undefined
        ) {
          this.revisionFlag[id] = true;
          this.revisionFlagTemp = false;
        } else {
          this.revisionFlag[id] = false;
        }
      }
    },
    revisionAvialable(size) {
      this.$emit("activeRevision", size);
    },
    RevisionBannerTogglerRevise(size) {
      this.revisionAvialable(size);
      this.$emit("goToGroupPage", true);
    },
    bannerValidation(restaurantObject) {
      var numberOfSatisfactoryRestaurants = 0;
      var revisionThreshold = 10;
      this.bannerToggle = true;
      const threshold = 0.6;
      const groupSize = Object.keys(this.groupInfo).length;
      for (var restaurant of Object.values(restaurantObject)) {
        const userList = Object.keys(this.groupInfo);
        var membersSatsfaction = false;
        var happyMembersCount = 0;
        for (const userKey of userList) {
          if (typeof this.attractiveness[userKey] === "undefined") {
            happyMembersCount++;
          } else if (
            this.attractiveness[userKey][JSON.parse(restaurant).id] > threshold
          ) {
            happyMembersCount++;
          }
        }
        if (happyMembersCount === groupSize) {
          this.bannerToggle = false;
          numberOfSatisfactoryRestaurants++;
        }
      }
      if (numberOfSatisfactoryRestaurants < revisionThreshold) {
        this.revisionTaggle = true;
      }
    },
    similarityExplanationFunc(restId) {
      this.similarityExplanation = "";
      const dataSimilarity = {
        restaurantId: restId,
        groupId: this.groupId,
      };
      const url = "http://46.18.25.97:8050/similarity/explanation";
      axios.post(url, dataSimilarity).then((response) => {
        this.simRestExp[restId] = JSON.parse(JSON.stringify(response.data));
        var similarityObj = JSON.parse(JSON.stringify(response.data));
        var explanation =
          "This restaurant is often chosen by groups that would also like to eat ";
        if (Object.keys(this.countPopularity).length === 0) {
          const url =
            "http://46.18.25.97:8050/recommendations/get/popularity/count";
          axios.get(url).then((response) => {
            var popularityCountObj = response.data;
            this.countPopularity = response.data;
            var indexCounter = 0;
            var flag = false;
            for (var pref of Object.keys(similarityObj)) {
              indexCounter++;
              var portion =
                parseFloat(similarityObj[pref]) /
                parseFloat(popularityCountObj[pref]);
              if (portion >= 1) {
                flag = true;
                explanation =
                  explanation +
                  "<b>" +
                  String(this.food_name_change(pref)) +
                  "</b>";
                // +
                // " <b>IS</b> a popoular preference";
                if (
                  Object.keys(similarityObj).length === 2 &&
                  Object.keys(similarityObj).length === indexCounter + 1
                ) {
                  explanation += " and ";
                }
                if (Object.keys(similarityObj).length === 1) {
                  explanation += " ";
                }
                if (
                  Object.keys(similarityObj).length > 2 &&
                  Object.keys(similarityObj).length > indexCounter + 1
                ) {
                  explanation += ", ";
                }
                if (
                  Object.keys(similarityObj).length > 2 &&
                  Object.keys(similarityObj).length === indexCounter + 1
                ) {
                  explanation += ", and ";
                } else {
                  explanation += " ";
                }
              }
              // else {
              //   explanation =
              //     explanation +
              //     "<b>" +
              //     String(this.food_name_change(pref)) +
              //     "</b>" +
              //     " is <b>NOT</b> a popoular preference";
              //   if (
              //     Object.keys(similarityObj).length === 2 &&
              //     Object.keys(similarityObj).length === indexCounter + 1
              //   ) {
              //     explanation += " and ";
              //   }
              //   if (Object.keys(similarityObj).length === 1) {
              //     explanation += " ";
              //   }
              //   if (
              //     Object.keys(similarityObj).length > 2 &&
              //     Object.keys(similarityObj).length > indexCounter + 1
              //   ) {
              //     explanation += ", ";
              //   }
              //   if (
              //     Object.keys(similarityObj).length > 2 &&
              //     Object.keys(similarityObj).length === indexCounter + 1
              //   ) {
              //     explanation += ", and ";
              //   } else {
              //     explanation += " ";
              //   }
              // }
            }
            explanation += ".";
            if (flag !== true) {
              explanation =
                "This restaurant is not very often chosen by groups that would like to eat the preferences that you have inserted for your group.";
            }
            explanation += "More precisely,";
            this.similarityExplanation = explanation;
            this.scoreDialog = ref(true);
          });
        } else {
          var popularityCountObj = this.countPopularity;
          var indexCounter = 0;
          var flag = false;
          for (var pref of Object.keys(similarityObj)) {
            indexCounter++;
            var portion =
              parseFloat(similarityObj[pref]) /
              parseFloat(popularityCountObj[pref]);
            if (portion >= 1) {
              flag = true;
              explanation =
                explanation +
                "<b>" +
                String(this.food_name_change(pref)) +
                "</b>";
              // +
              // " <b>IS</b> a popoular preference";
              if (
                Object.keys(similarityObj).length === 2 &&
                Object.keys(similarityObj).length === indexCounter + 1
              ) {
                explanation += " and ";
              }
              if (Object.keys(similarityObj).length === 1) {
                explanation += " ";
              }
              if (
                Object.keys(similarityObj).length > 2 &&
                Object.keys(similarityObj).length > indexCounter + 1
              ) {
                explanation += ", ";
              }
              if (
                Object.keys(similarityObj).length > 2 &&
                Object.keys(similarityObj).length === indexCounter + 1
              ) {
                explanation += ", and ";
              } else {
                explanation += " ";
              }
            }
            // else {
            //   explanation =
            //     explanation +
            //     "<b>" +
            //     String(this.food_name_change(pref)) +
            //     "</b>" +
            //     " is <b>NOT</b> a popoular preference";
            //   if (
            //     Object.keys(similarityObj).length === 2 &&
            //     Object.keys(similarityObj).length === indexCounter + 1
            //   ) {
            //     explanation += " and ";
            //   }
            //   if (Object.keys(similarityObj).length === 1) {
            //     explanation += " ";
            //   }
            //   if (
            //     Object.keys(similarityObj).length > 2 &&
            //     Object.keys(similarityObj).length > indexCounter + 1
            //   ) {
            //     explanation += ", ";
            //   }
            //   if (
            //     Object.keys(similarityObj).length > 2 &&
            //     Object.keys(similarityObj).length === indexCounter + 1
            //   ) {
            //     explanation += ", and ";
            //   } else {
            //     explanation += " ";
            //   }
            // }
          }
          explanation += ".";
          if (flag !== true) {
            explanation =
              "This restaurant is not very often chosen by groups that would like to eat the preferences that you have inserted for your group.";
          }
          explanation += "More precisely,";
          this.similarityExplanation = explanation;
          this.scoreDialog = ref(true);
        }
      });
    },
    popPercentage(getRestId) {
      if (this.popularityModel[getRestId] === 5) {
        return "This restaurant is the <strong>MOST</strong> popular restaurant in this application.";
      } else if (this.popularityModel[getRestId] === 0) {
        return "This is <strong>NOT</strong> a popular restaurant in our application.";
      } else {
        var min = 1000;
        var max = 0;
        var counter = 0;
        var comparison = 0;
        for (var restPop of Object.values(this.popularityObj)) {
          if (
            parseFloat(this.popularityObj[getRestId]) >= parseFloat(restPop)
          ) {
            comparison++;
          }
          counter++;
        }
        var portion = String(parseFloat(comparison / counter).toFixed(2) * 100);
        var normalizedValue = (parseFloat(restPop) - min) / (max - min);
        var exp =
          "This is more popular than <strong>" +
          portion +
          "%</strong> restaurants  in our application.";
        return exp;
      }
    },
    populairtyModelFunc() {
      var popularityObjTemp = {};
      var counter = 0;
      if (JSON.parse(sessionStorage.getItem("popularityValidation")) !== true) {
        for (var resturant of Object.values(this.restaurantJson)) {
          var restIdGet = JSON.parse(resturant).id;
          var url =
            "http://46.18.25.97:8050/restaurant/popularity/dict/" +
            String(restIdGet);
          axios.get(url).then((response) => {
            popularityObjTemp[parseInt(Object.keys(response.data)[0])] =
              parseFloat(Object.values(response.data)[0]);
            counter++;
            if (counter === this.restaurantJson.length) {
              var min = Math.min.apply(Math, Object.values(popularityObjTemp));
              var max = Math.max.apply(Math, Object.values(popularityObjTemp));
              for (var resturant of Object.keys(popularityObjTemp)) {
                var normalizedValue =
                  (parseFloat(popularityObjTemp[resturant]) - min) /
                  (max - min);
                if (normalizedValue <= 0) {
                  this.popularityModel[resturant] = ref(0);
                } else if (normalizedValue <= 0.2) {
                  this.popularityModel[resturant] = ref(1);
                } else if (normalizedValue <= 0.4) {
                  this.popularityModel[resturant] = ref(2);
                } else if (normalizedValue <= 0.6) {
                  this.popularityModel[resturant] = ref(3);
                } else if (normalizedValue <= 0.8) {
                  this.popularityModel[resturant] = ref(4);
                } else {
                  this.popularityModel[resturant] = ref(5);
                }
              }
              this.popularityObj = popularityObjTemp;
              sessionStorage.setItem(
                "popularityObj",
                JSON.stringify(this.popularityObj)
              );
              sessionStorage.setItem("popularityValidation", true);
              this.popularityModelLoad = true;
            }
          });
        }
      } else {
        popularityObjTemp = JSON.parse(sessionStorage.getItem("popularityObj"));
        var min = Math.min.apply(Math, Object.values(popularityObjTemp));
        var max = Math.max.apply(Math, Object.values(popularityObjTemp));
        for (var resturant of Object.keys(popularityObjTemp)) {
          var normalizedValue =
            (parseFloat(popularityObjTemp[resturant]) - min) / (max - min);
          if (normalizedValue <= 0) {
            this.popularityModel[resturant] = ref(0);
          } else if (normalizedValue <= 0.2) {
            this.popularityModel[resturant] = ref(1);
          } else if (normalizedValue <= 0.4) {
            this.popularityModel[resturant] = ref(2);
          } else if (normalizedValue <= 0.6) {
            this.popularityModel[resturant] = ref(3);
          } else if (normalizedValue <= 0.8) {
            this.popularityModel[resturant] = ref(4);
          } else {
            this.popularityModel[resturant] = ref(5);
          }
        }
        this.popularityModelLoad = true;
      }
    },
    scrollToTop() {
      window.scrollTo(0, 0);
    },
    scoreDialogFunc(dialogType, restIdGet) {
      var usrId = 0;
      for (var [key, value] of Object.entries(this.groupInfo)) {
        if (value[0] === "organizer") {
          usrId = key;
        }
      }

      var explainStorage = { user_id: usrId, group_id: this.groupId };
      if (dialogType === "pop") {
        explainStorage["popularity"] = true;
        axios
          .post(
            "http://46.18.25.97:8050/interaction/explain/storage",
            explainStorage
          )
          .then();
        this.scoreDialog = ref(true);
        this.scoreExplanation = "pop";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting Popularity Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (dialogType === "avrattr") {
        explainStorage["fitness"] = true;
        axios
          .post(
            "http://46.18.25.97:8050/interaction/explain/storage",
            explainStorage
          )
          .then();
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting Average attractiveness Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
        this.scoreDialog = ref(true);
        this.scoreExplanation = "avrattr";
      } else if (dialogType === "fair") {
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting Fairness Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
        this.scoreDialog = ref(true);
        this.extractDissatisfieds(restIdGet);
        this.scoreExplanation = "fair";
      } else if (dialogType === "attrfair") {
        var interactionData = {
          group_id: this.group_id_intract,
          interaction:
            "Visiting Fairness and Average Attractiveness Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
        this.scoreDialog = ref(true);
        this.scoreExplanation = "attrfair";
      } else if (dialogType === "sim") {
        explainStorage["sim"] = true;
        axios
          .post(
            "http://46.18.25.97:8050/interaction/explain/storage",
            explainStorage
          )
          .then();
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting Similarity Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
        this.similarityExplanationFunc(restIdGet);
        this.scoreExplanation = "sim";
      } else if (dialogType === "trip") {
        explainStorage["trip"] = true;
        axios
          .post(
            "http://46.18.25.97:8050/interaction/explain/storage",
            explainStorage
          )
          .then();
        this.scoreExplanation = "trip";
        this.scoreDialog = ref(true);
      } else if (dialogType === "dishDiv") {
        explainStorage["dish"] = true;
        axios
          .post(
            "http://46.18.25.97:8050/interaction/explain/storage",
            explainStorage
          )
          .then();
        this.scoreExplanation = "dishDiv";
        this.scoreDialog = ref(true);
      } else if (dialogType === "categ") {
        explainStorage["category"] = true;
        axios
          .post(
            "http://46.18.25.97:8050/interaction/explain/storage",
            explainStorage
          )
          .then();
        this.scoreExplanation = "categ";
        this.scoreDialog = ref(true);
      }
    },
    getSimilarityLevel(restIdGet) {
      if (this.similarityModel[restIdGet] <= 0) {
        return "NOT SIMILAR";
      } else if (this.similarityModel[restIdGet] <= 1.5) {
        return "BARELY SIMILAR";
      } else if (this.similarityModel[restIdGet] <= 2.5) {
        return "PARTIALLY SIMILAR";
      } else if (this.similarityModel[restIdGet] <= 3.5) {
        return "SIMILAR";
      } else if (this.similarityModel[restIdGet] <= 4.5) {
        return "VERY SIMILAR";
      } else if (this.similarityModel[restIdGet] <= 5) {
        return "PERFECTLY SIMILAR";
      }
    },
    getRange() {
      if (this.critiqueRange === "eco") {
        return "Economic";
      } else if (this.critiqueRange === "mid") {
        return "Mid-range";
      }
      if (this.critiqueRange === "exp") {
        return "Expensive";
      } else {
        return "All Prices";
      }
    },
    goToGrpPage() {
      this.$emit("goToGroupPage");
    },
    newSessoin() {
      location.reload();
    },
    storeGeneralInteraction() {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Visiting General Scores",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
    },
    storeGroupInteraction() {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Visiting Group Scores",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
    },
    storeIndividualInteraction() {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Visiting Individual Scores",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
    },
    openPriceCritique() {
      this.positionPrice = ref("bottom");
      this.priceDialog = ref(true);
    },
    open(pos) {
      this.position = ref("bottom");
      this.sortDialog = ref(true);
    },
    async sorting(sorting_id, user_id, name, callback) {
      var usrId = 0;
      for (var [key, value] of Object.entries(this.groupInfo)) {
        if (value[0] === "organizer") {
          usrId = key;
        }
      }
      var interactionSorting = {
        user_id: usrId,
        group_id: this.groupId,
        sorting_book: false,
        sorting_fit: false,
        sorting_sim: false,
      };
      var popularityRanking = [];
      for (var key in this.restaurantJson) {
        popularityRanking.push(JSON.parse(this.restaurantJson[key]).id);
      }
      popularityRanking.reverse();
      if (sorting_id === 0) {
        if (this.groupInfo[user_id][1] === "Organizer") {
          var tempname = "your";
        } else {
          var tempname = this.groupInfo[user_id][1];
        }
        sessionStorage.setItem("sorting", 0);
        if (user_id === 0) {
          user_id = sessionStorage.getItem("userSorting");
          this.sortType = "Sort: By " + tempname + " preference";
          this.sortActive = true;
        } else {
          sessionStorage.setItem("userSorting", user_id);
          this.sortType = "Sort: By " + tempname + " preference";
          this.sortActive = true;
        }
        // for user-based sorting
        var user_attractiveness = this.attractiveness[user_id];
        let sortable = [];
        for (var rest in user_attractiveness) {
          var rest_fairness = this.fariness(rest);
          sortable.push([
            rest,
            user_attractiveness[rest] +
              rest_fairness / 100 +
              popularityRanking.indexOf(rest) / 100000,
          ]);
        }
        sortable.sort(function (a, b) {
          return a[1] - b[1];
        });
        sortable = sortable.reverse();
        var new_restRel = [];
        for (var item of sortable) {
          for (var object in this.restaurantJsonRel) {
            if (
              parseInt(JSON.parse(this.restaurantJsonRel[object]).id) ===
              parseInt(item[0])
            ) {
              new_restRel.push(this.restaurantJsonRel[object]);
            }
          }
        }
        this.sortLabel = "Sort: By " + String(name) + " preference";
        this.restaurantJsonRel = new_restRel;
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Sort: By " + String(name) + " preference",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
        this.sortUserId = user_id;
        sessionStorage.setItem("user_id", user_id);
        this.sortingType = "attr";
      } else if (sorting_id === 1) {
        this.sortingType = "fair";
        sessionStorage.setItem("sorting", 1);
        this.sortType = "Sort: By minimizing individual dissatisfaction";
        this.sortActive = true;
        let sortable = [];
        var organizer_id = Object.keys(this.groupInfo)[0];
        this.avergeAttr();
        // this.organizer_user_attractiveness = this.attractiveness[organizer_id];
        for (var object in this.restaurantJsonRel) {
          if (
            this.organizer_user_attractiveness[
              JSON.parse(this.restaurantJsonRel[object]).id
            ] === 0
          ) {
            sortable.push([
              JSON.parse(this.restaurantJsonRel[object]).id,
              this.avrAttract[JSON.parse(this.restaurantJsonRel[object]).id] /
                100 +
                popularityRanking.indexOf(
                  JSON.parse(this.restaurantJsonRel[object]).id
                ) /
                  100000,
            ]);
          } else {
            sortable.push([
              JSON.parse(this.restaurantJsonRel[object]).id,
              this.fariness(JSON.parse(this.restaurantJsonRel[object]).id) +
                this.avrAttract[JSON.parse(this.restaurantJsonRel[object]).id] /
                  100 +
                popularityRanking.indexOf(
                  JSON.parse(this.restaurantJsonRel[object]).id
                ) /
                  100000,
            ]);
          }
        }
        sortable.sort(function (a, b) {
          return a[1] - b[1];
        });
        sortable = sortable.reverse();
        var new_restRel = [];
        for (var item of sortable) {
          for (var object in this.restaurantJsonRel) {
            if (
              parseInt(JSON.parse(this.restaurantJsonRel[object]).id) ===
              parseInt(item[0])
            ) {
              new_restRel.push(this.restaurantJsonRel[object]);
            }
          }
        }
        this.restaurantJsonRel = new_restRel;
        this.sortLabel = "Sort: By minimizing individual dissatisfaction";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Sort: By fairness",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (sorting_id === 2) {
        this.sortingType = "attrfair";
        this.sortType = "Sort: By fairness & attractiveness";
        this.sortActive = true;
        sessionStorage.setItem("sorting", 2);
        let sortable = [];
        for (var object in this.restaurantJsonRel) {
          var counter = 0;
          var sum = 0;
          for (var user in this.groupInfo) {
            if (Object.keys(this.attractiveness).includes(user)) {
              sum =
                sum +
                this.attractiveness[user][
                  JSON.parse(this.restaurantJsonRel[object]).id
                ];
              counter++;
            }
          }
          sortable.push([
            JSON.parse(this.restaurantJsonRel[object]).id,
            this.fariness(JSON.parse(this.restaurantJsonRel[object]).id) *
              (sum / counter),
          ]);
        }
        sortable.sort(function (a, b) {
          return a[1] - b[1];
        });
        sortable = sortable.reverse();
        var new_restRel = [];
        for (var item of sortable) {
          for (var object in this.restaurantJsonRel) {
            if (
              parseInt(JSON.parse(this.restaurantJsonRel[object]).id) ===
              parseInt(item[0])
            ) {
              new_restRel.push(this.restaurantJsonRel[object]);
            }
          }
        }
        this.restaurantJsonRel = new_restRel;
        this.sortLabel = "Sort: By fairness and Attractiveness";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Sort: By fairness and Attractiveness",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (sorting_id === 4) {
        interactionSorting["sorting_fit"] = true;
        this.sortingType = "avrattr";
        this.sortType = "Sort: By maximizing group satisfaction";
        this.sortActive = true;
        sessionStorage.setItem("sorting", 4);
        this.avergeAttr();
        let sortable = [];
        for (var object in this.restaurantJsonRel) {
          var menuSizeRestIn =
            this.menuSizeRest[JSON.parse(this.restaurantJsonRel[object]).id];
          sortable.push([
            JSON.parse(this.restaurantJsonRel[object]).id,
            this.avrAttract[JSON.parse(this.restaurantJsonRel[object]).id] +
              menuSizeRestIn["category"] / 1000 +
              menuSizeRestIn["dishes"] / 100000,
          ]);
        }
        sortable.sort(function (a, b) {
          return a[1] - b[1];
        });
        sortable = sortable.reverse();
        var new_restRel = [];
        for (var item of sortable) {
          for (var object in this.restaurantJsonRel) {
            if (
              parseInt(JSON.parse(this.restaurantJsonRel[object]).id) ===
              parseInt(item[0])
            ) {
              new_restRel.push(this.restaurantJsonRel[object]);
            }
          }
        }
        this.restaurantJsonRel = new_restRel;
        this.sortLabel = "Sort: By Maximizing group satisfaction";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Sort: By average Attractiveness",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (sorting_id === 5) {
        interactionSorting["sorting_sim"] = true;
        this.sortingType = "sim";
        this.sortType =
          "Sort: by Similarity to the group which bookmarked restaurants";
        this.sortActive = true;
        sessionStorage.setItem("sorting", 5);
        let sortable = [];
        for (var object in this.restaurantJsonRel) {
          sortable.push([
            JSON.parse(this.restaurantJsonRel[object]).id,
            this.similarityValue[JSON.parse(this.restaurantJsonRel[object]).id],
          ]);
        }
        sortable.sort(function (a, b) {
          return a[1] - b[1];
        });
        sortable = sortable.reverse();
        var new_restRel = [];
        for (var item of sortable) {
          for (var object in this.restaurantJsonRel) {
            if (
              parseInt(JSON.parse(this.restaurantJsonRel[object]).id) ===
              parseInt(item[0])
            ) {
              new_restRel.push(this.restaurantJsonRel[object]);
            }
          }
        }
        this.restaurantJsonRel = new_restRel;
        this.sortLabel =
          "Sort by Similarity to the group which bookmarked restaurants";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction:
            "Sort: by Similarity to the group which bookmarked restaurants",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
        // this.sortLabel = "Sorted by popularith among the group like you";
      } else if (sorting_id === -1) {
        interactionSorting["sorting_book"] = true;
        this.sortingType = "pop";
        sessionStorage.setItem("sorting", -1);
        this.restaurantJsonRel = this.restaurantJson;
        this.sortType = "Sort: By populairty";
        this.sortActive = true;
      }
      axios
        .post(
          "http://46.18.25.97:8050/interaction/sort/storage",
          interactionSorting
        )
        .then();
    },
    menuSize(restId, counterStop) {
      if (this.menuSizeValidity !== true) {
        var sizeOfCategory = 0;
        var sizeOfDishes = 0;
        const urlmnue = "http://46.18.25.97:8050/restaurant/menu/" + restId;
        axios.get(urlmnue).then((response) => {
          var menuList = JSON.parse(JSON.stringify(response.data));
          for (var category of Object.keys(menuList)) {
            if (menuList[category].length > 0) {
              sizeOfCategory++;
            }
            sizeOfDishes += menuList[category].length;
          }
          this.menuSizeRest[restId] = {
            category: sizeOfCategory,
            dishes: sizeOfDishes,
          };
          if (this.restaurantJsonRel.length === counterStop) {
            this.menuSizeValidity = true;
            sessionStorage.setItem(
              "MenuSize",
              JSON.stringify(this.menuSizeRest)
            );
            sessionStorage.setItem("menuSizeValidity", true);
          }
        });
      }
    },
    fairness_attractiveness() {
      var fair_attract_max = 0;
      if (Object.keys(this.groupInfo).length === 1) {
        this.fair_attract = this.attractiveness[Object.keys(this.groupInfo)];
        return;
      }
      for (var object in this.restaurantJsonRel) {
        var counter = 0;
        var sum = 0;
        for (var user in this.groupInfo) {
          if (Object.keys(this.attractiveness).includes(user)) {
            sum =
              sum +
              this.attractiveness[user][
                JSON.parse(this.restaurantJsonRel[object]).id
              ];
            counter++;
          }
        }
        this.fair_attract[JSON.parse(this.restaurantJsonRel[object]).id] =
          this.fariness(JSON.parse(this.restaurantJsonRel[object]).id) *
          (sum / counter);
        if (
          fair_attract_max <
          this.fariness(JSON.parse(this.restaurantJsonRel[object]).id) *
            (sum / counter)
        ) {
          fair_attract_max =
            this.fariness(JSON.parse(this.restaurantJsonRel[object]).id) *
            (sum / counter);
        }
      }
      for (var item in this.fair_attract) {
        this.fair_attract[item] = this.fair_attract[item] / fair_attract_max;
      }
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
    popularity(restId) {
      var url =
        "http://46.18.25.97:8050/restaurant/popularity/" + String(restId);
      axios.get(url).then((response) => {
        this.popularityObj[restId] = parseFloat(JSON.parse(response.data));
        sessionStorage.setItem(
          "popularityObj",
          JSON.stringify(this.popularityObj)
        );

        return parseFloat(JSON.parse(response.data));
      });
    },
    selectedPopularity(restId) {
      this.selectLoad[restId] = false;
      // this.selectedPopularityObj[restId] = 0;
      var url =
        "http://46.18.25.97:8050/restaurant/select/popularity/" +
        String(restId);
      axios.get(url).then((response) => {
        this.selectedPopularityObj[restId] = parseFloat(
          JSON.parse(response.data)
        );
        this.selectLoad[restId] = true;
        sessionStorage.setItem(
          "selectedPopularity",
          JSON.stringify(this.selectedPopularityObj)
        );
      });
    },
    requiringIcon(type) {
      if (type == "half") {
        const required = require(`../assets/half_circle.png`);
        return "img:" + required;
      } else if (type == "full") {
        const required = require(`../assets/full_circle.png`);
        return "img:" + required;
      } else {
        const required = require(`../assets/border_circle.png`);
        return "img:" + required;
      }
    },
    getLogo(logo) {
      return require(`../assets/logo/` + String(logo));
    },
    getLogoIn(logo) {
      return require(`../assets/logo/logo/` + String(logo));
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
        var usrId = 0;
        for (var [key, value] of Object.entries(this.groupInfo)) {
          if (value[0] === "organizer") {
            usrId = key;
          }
        }
        var tempCounter = 0;
        var index = -1;
        for (var tempRestValue of Object.keys(this.restaurantJsonRel)) {
          tempCounter++;
          if (
            parseInt(
              JSON.parse(this.restaurantJsonRel[tempRestValue])["id"]
            ) === restaurantId
          ) {
            index = tempCounter;
          }
        }
        var bookingInteractionData = {
          user_id: parseInt(usrId),
          group_id: this.group_id_intract,
          rest_id: restaurantId,
          avialble_rest: this.currentRestaurant,
          sort_pop: this.sortingType === "pop",
          sort_fit: this.sortingType === "avrattr",
          sort_sim: this.sortingType === "sim",
          fit_score:
            this.avrAttract[restaurantId] === undefined
              ? -1
              : this.avrAttract[restaurantId],
          sim_score:
            this.similarityValue[restaurantId] === undefined
              ? -1
              : this.similarityValue[restaurantId],
          fit_rank: this.sortingType === "avrattr" ? index : -1,
          sim_rank: this.sortingType === "sim" ? index : -1,
          pop_rank: this.sortingType === "pop" ? index : -1,
          tip: this.tripScore[restaurantId],
          category: this.menuSizeRest[restaurantId]["category"] / 10,
          dish: this.menuSizeRest[restaurantId]["dishes"],
          price: "str",
        };
        var tempUser = ["c1_fit", "c2_fit", "c3_fit", "c4_fit", "c5_fit"];
        for (var itUsr of Object.keys(this.groupInfo)) {
          if (this.attractiveness[itUsr] !== undefined) {
            bookingInteractionData[tempUser.shift()] =
              this.attractiveness[itUsr][restaurantId];
          }
        }
        axios
          .post(
            "http://46.18.25.97:8050/interaction/book/storage",
            bookingInteractionData
          )
          .then();
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
      var usrId = 0;
      for (var [key, value] of Object.entries(this.groupInfo)) {
        if (value[0] === "organizer") {
          usrId = key;
        }
      }
      var tempCounter = 0;
      var index = -1;
      for (var tempRestValue of Object.keys(this.restaurantJsonRel)) {
        tempCounter++;
        if (
          parseInt(JSON.parse(this.restaurantJsonRel[tempRestValue])["id"]) ===
          JSON.parse(rest).id
        ) {
          index = tempCounter;
        }
      }
      var visitingInteractionData = {
        user_id: parseInt(usrId),
        group_id: this.group_id_intract,
        rest_id: JSON.parse(rest).id,
        avialble_rest: this.currentRestaurant,
        sort_pop: this.sortingType === "pop",
        sort_fit: this.sortingType === "avrattr",
        sort_sim: this.sortingType === "sim",
        fit_score:
          this.avrAttract[JSON.parse(rest).id] === undefined
            ? -1
            : this.avrAttract[JSON.parse(rest).id],
        sim_score:
          this.similarityValue[JSON.parse(rest).id] === undefined
            ? -1
            : this.similarityValue[JSON.parse(rest).id],
        fit_rank: this.sortingType === "avrattr" ? index : -1,
        sim_rank: this.sortingType === "sim" ? index : -1,
        pop_rank: this.sortingType === "pop" ? index : -1,
        tip: this.tripScore[JSON.parse(rest).id],
        category: this.menuSizeRest[JSON.parse(rest).id]["category"] / 10,
        dish: this.menuSizeRest[JSON.parse(rest).id]["dishes"],
        price: "str",
      };
      var tempUser = ["c1_fit", "c2_fit", "c3_fit", "c4_fit", "c5_fit"];
      for (var itUsr of Object.keys(this.groupInfo)) {
        if (this.attractiveness[itUsr] !== undefined) {
          visitingInteractionData[tempUser.shift()] =
            this.attractiveness[itUsr][JSON.parse(rest).id];
        }
      }
      axios
        .post(
          "http://46.18.25.97:8050/interaction/visited/storage",
          visitingInteractionData
        )
        .then();
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
    getSimilarity(restaurantId, counter) {
      var all_data = {};
      if (this.restaurantJsonRel.length) {
        var rests_ids = [];
        // for (var tempRestValue of Object.keys(this.restaurantJsonRel)) {
        //   rests_ids.push(
        //     parseInt(JSON.parse(this.restaurantJsonRel[tempRestValue])["id"])
        //   );
        // }
        // const url_all = "http://46.18.25.97:8050/similarity/all";
        // var dataSimilarityAll = {
        //   restaurantId: rests_ids,
        //   groupId: this.groupId,
        // };
        // axios.post(url_all, dataSimilarityAll).then((response) => {
        //  all_data = response.data;
        // });

        //  for (var [key,value] of Object.entries(all_data)) {
        //     const dataSimilarity = {
        //     restaurantId: restaurantId,
        //     groupId: this.groupId,
        //   };
        //   const url = "http://46.18.25.97:8050/similarity";
        //   axios.post(url, dataSimilarity).then((response) => {
        //     if (response.data !== null) {
        //       var sutiability = 0;
        //       const dataSimilarity = {
        //         restaurantId: restaurantId,
        //         groupId: this.groupId,
        //       };
        //       const url = "http://46.18.25.97:8050/similarity/explanation";
        //       axios.post(url, dataSimilarity).then((response) => {
        //         this.simRestExp[restaurantId] = JSON.parse(
        //           JSON.stringify(response.data)
        //         );

        //         var similarityObj = JSON.parse(JSON.stringify(response.data));
        //         if (Object.keys(this.countPopularity).length === 0) {
        //           const url =
        //             "http://46.18.25.97:8050/recommendations/get/popularity/count";
        //           axios.get(url).then((response) => {
        //             var counterHere = counter;
        //             var popularityCountObj = response.data;
        //             this.countPopularity = response.data;
        //             var indexCounter = 0;
        //             var flag = false;
        //             for (var pref of Object.keys(similarityObj)) {
        //               indexCounter++;
        //               var portion =
        //                 parseFloat(similarityObj[pref]) /
        //                 parseFloat(popularityCountObj[pref]);
        //               if (portion >= 1) {
        //                 sutiability++;
        //               }
        //             }
        //             sutiability = sutiability / Object.keys(similarityObj).length;
        //             this.similarityValue[restaurantId] = sutiability;
        //             this.similarityModelFunc(restaurantId, sutiability);
        //             if (this.restaurantJsonRel.length === counterHere) {
        //               this.similarityValidity = true;
        //               sessionStorage.setItem(
        //                 "SimilarityValue",
        //                 JSON.stringify(this.similarityValue)
        //               );
        //               sessionStorage.setItem("SimilarityValidation", true);
        //             }
        //           });
        //         } else {
        //           var counterHere = counter;
        //           var popularityCountObj = this.countPopularity;
        //           var indexCounter = 0;
        //           var flag = false;
        //           for (var pref of Object.keys(similarityObj)) {
        //             indexCounter++;
        //             var portion =
        //               parseFloat(similarityObj[pref]) /
        //               parseFloat(popularityCountObj[pref]);
        //             if (portion >= 1) {
        //               sutiability++;
        //             }
        //           }
        //           sutiability = sutiability / Object.keys(similarityObj).length;
        //           this.similarityValue[restaurantId] = sutiability;
        //           this.similarityModelFunc(restaurantId, sutiability);
        //           if (this.restaurantJsonRel.length === counterHere) {
        //             this.similarityValidity = true;
        //             sessionStorage.setItem(
        //               "SimilarityValue",
        //               JSON.stringify(this.similarityValue)
        //             );
        //             sessionStorage.setItem("SimilarityValidation", true);
        //           }
        //         }
        //       });
        //     } else {
        //       this.similarityValue[restaurantId] = 0;
        //       this.similarityModelFunc(restaurantId, 0);
        //     }
        //     // if (Object.keys(this.similarityValue).length === counter) {
        //     //   this.similarityValidity = true;
        //     //   sessionStorage.setItem(
        //     //     "SimilarityValue",
        //     //     JSON.stringify(this.similarityValue)
        //     //   );
        //     //   sessionStorage.setItem("SimilarityValidation", true);
        //     // }
        //   });
        //  }

        const dataSimilarity = {
          restaurantId: restaurantId,
          groupId: this.groupId,
        };
        const url = "http://46.18.25.97:8050/similarity";
        axios.post(url, dataSimilarity).then((response) => {
          if (response.data !== null) {
            var sutiability = 0;
            const dataSimilarity = {
              restaurantId: restaurantId,
              groupId: this.groupId,
            };
            const url = "http://46.18.25.97:8050/similarity/explanation";
            axios.post(url, dataSimilarity).then((response) => {
              this.simRestExp[restaurantId] = JSON.parse(
                JSON.stringify(response.data)
              );

              var similarityObj = JSON.parse(JSON.stringify(response.data));
              if (Object.keys(this.countPopularity).length === 0) {
                const url =
                  "http://46.18.25.97:8050/recommendations/get/popularity/count";
                axios.get(url).then((response) => {
                  var counterHere = counter;
                  var popularityCountObj = response.data;
                  this.countPopularity = response.data;
                  var indexCounter = 0;
                  var flag = false;
                  for (var pref of Object.keys(similarityObj)) {
                    indexCounter++;
                    var portion =
                      parseFloat(similarityObj[pref]) /
                      parseFloat(popularityCountObj[pref]);
                    if (portion >= 1) {
                      sutiability++;
                    }
                  }
                  sutiability = sutiability / Object.keys(similarityObj).length;
                  this.similarityValue[restaurantId] = sutiability;
                  this.similarityModelFunc(restaurantId, sutiability);
                  if (this.restaurantJsonRel.length === counterHere) {
                    this.similarityValidity = true;
                    sessionStorage.setItem(
                      "SimilarityValue",
                      JSON.stringify(this.similarityValue)
                    );
                    sessionStorage.setItem("SimilarityValidation", true);
                  }
                });
              } else {
                var counterHere = counter;
                var popularityCountObj = this.countPopularity;
                var indexCounter = 0;
                var flag = false;
                for (var pref of Object.keys(similarityObj)) {
                  indexCounter++;
                  var portion =
                    parseFloat(similarityObj[pref]) /
                    parseFloat(popularityCountObj[pref]);
                  if (portion >= 1) {
                    sutiability++;
                  }
                }
                sutiability = sutiability / Object.keys(similarityObj).length;
                this.similarityValue[restaurantId] = sutiability;
                this.similarityModelFunc(restaurantId, sutiability);
                if (this.restaurantJsonRel.length === counterHere) {
                  this.similarityValidity = true;
                  sessionStorage.setItem(
                    "SimilarityValue",
                    JSON.stringify(this.similarityValue)
                  );
                  sessionStorage.setItem("SimilarityValidation", true);
                }
              }
            });
          } else {
            this.similarityValue[restaurantId] = 0;
            this.similarityModelFunc(restaurantId, 0);
          }
          // if (Object.keys(this.similarityValue).length === counter) {
          //   this.similarityValidity = true;
          //   sessionStorage.setItem(
          //     "SimilarityValue",
          //     JSON.stringify(this.similarityValue)
          //   );
          //   sessionStorage.setItem("SimilarityValidation", true);
          // }
        });
      }
    },
    fariness(restId) {
      // if (this.restaurantJsonRel.length) {
      //   if (Object.keys(this.groupInfo).length === 1) {
      //     return this.attractiveness[Object.keys(this.groupInfo)][restId];
      //   }
      //   var groupRelevance = {};
      //   const userList = Object.keys(this.groupInfo);
      //   for (const userKey of userList) {
      //     if (
      //       Object.keys(this.attractiveness).length != 0 &&
      //       this.attractiveness[userKey] != undefined
      //     ) {
      //       groupRelevance[userKey] = this.attractiveness[userKey][restId];
      //     }
      //   }
      //   var fairList = Object.values(groupRelevance);
      //   if (fairList.length > 0) {
      //     if (this.standardDeviation(fairList) > 0) {
      //       // var avr = fairList.reduce((a, b) => a + b, 0) / fairList.length;
      //       // const reverseVariance = 1 - this.standardDeviation(fairList) / avr;
      //       const reverseVariance = 1 - this.manhatanDistance(fairList);
      //       return reverseVariance;
      //     } else {
      //       var organizer_id = Object.keys(this.groupInfo)[0];
      //       if (this.attractiveness[organizer_id][restId] === 0) {
      //         return 0;
      //       } else {
      //         return 1;
      //       }
      //     }
      //   } else {
      //     return 0;
      //   }
      // }
      return this.extractDissatisfieds(restId);
    },
    manhatanDistance(attractList) {
      var manhatanDistVariable = 0;
      var counter = 0;
      for (let outerIndex = 0; outerIndex < attractList.length; outerIndex++) {
        for (
          let innerIndex = outerIndex + 1;
          innerIndex < attractList.length;
          innerIndex++
        ) {
          counter++;
          manhatanDistVariable =
            manhatanDistVariable +
            Math.abs(attractList[outerIndex] - attractList[innerIndex]);
        }
      }
      var finalManhatan = manhatanDistVariable / counter;
      return finalManhatan;
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
    extractDissatisfieds(restId) {
      this.happyValidator = false;
      this.sadValidator = false;
      var threshold = 0.6;
      var numberOfSads = 0;
      var numberOfHappies = 0;
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
            this.userAttractive[userKey] = [
              this.groupInfo[userKey][0] === "organizer"
                ? "blue"
                : this.groupInfo[userKey][0],
              this.attractiveness[userKey][restId] > threshold ? 1 : -1,
              this.groupInfo[userKey][1] === "Organizer"
                ? "you"
                : this.groupInfo[userKey][1],
            ];
            if (this.attractiveness[userKey][restId] > threshold) {
              numberOfHappies++;
              this.happyValidator = true;
            } else {
              numberOfSads++;
              this.sadValidator = true;
            }
          }
        }
        if (numberOfSads + numberOfHappies > 0) {
          if (numberOfHappies > 0) {
            if (userList.length === 1) {
              return numberOfHappies / (numberOfSads + numberOfHappies);
            } else if (userList.length === 2) {
              return (
                (numberOfHappies / (numberOfSads + numberOfHappies) - 1 / 2) /
                0.5
              );
            } else if (userList.length === 3) {
              return (
                (numberOfHappies / (numberOfSads + numberOfHappies) - 1 / 3) /
                (1 - 1 / 3)
              );
            } else if (userList.length === 4) {
              return (
                (numberOfHappies / (numberOfSads + numberOfHappies) - 1 / 4) /
                (1 - 1 / 4)
              );
            } else {
              return (
                (numberOfHappies / (numberOfSads + numberOfHappies) - 1 / 5) /
                (1 - 1 / 5)
              );
            }
          } else {
            return 0;
          }
        } else {
          return 0;
        }
      }
    },
    extractDissatisfiedsAbsolutNumbers(restId) {
      var tempList = [];
      var threshold = 0.6;
      var numberOfSads = 0;
      var numberOfHappies = 0;
      if (this.restaurantJsonRel.length) {
        // if (Object.keys(this.groupInfo).length === 1) {
        //   return this.attractiveness[Object.keys(this.groupInfo)][restId];
        // }
        var groupRelevance = {};
        const userList = Object.keys(this.groupInfo);
        for (const userKey of userList) {
          if (
            Object.keys(this.attractiveness).length != 0 &&
            this.attractiveness[userKey] != undefined
          ) {
            groupRelevance[userKey] = this.attractiveness[userKey][restId];
            if (this.attractiveness[userKey][restId] > threshold) {
              numberOfHappies++;
            } else {
              numberOfSads++;
              if (this.groupInfo[userKey][0] === "organizer") {
                tempList.push("you");
              } else {
                tempList.push(this.groupInfo[userKey][1]);
              }
            }
          }
        }
        var tempExplanationSadness = "";
        if (tempList.length === 1) {
          tempExplanationSadness =
            tempList[0] + " will not be satisfied with this restaurant.";
        } else if (tempList.length === 2) {
          tempExplanationSadness =
            tempList[0] +
            " and " +
            tempList[1] +
            " will not be satisfied with this restaurant.";
        } else {
          var counterSad = 0;
          tempExplanationSadness = "";
          for (var user of tempList) {
            counterSad++;
            if (counterSad < tempList.length - 2) {
              tempExplanationSadness = tempExplanationSadness + user + ", ";
            } else if (counterSad === tempList.length - 1) {
              tempExplanationSadness = tempExplanationSadness + user + ", and ";
            } else {
              tempExplanationSadness = tempExplanationSadness + user + " ";
            }
          }
          tempExplanationSadness +=
            "will not be satisfied with this restaurant.";
        }
        if (tempList.length === Object.keys(this.groupInfo).length) {
          tempExplanationSadness =
            "None of the group members will be satisfied with this restaurant.";
        }
        this.sadsList[restId] = tempExplanationSadness;
        var stringfyNumHappy = "";
        var stringfyNumSad = "";
        if (numberOfHappies === 0) {
          stringfyNumHappy = "NONE";
        } else {
          stringfyNumHappy = this.digitToWord(parseInt(numberOfHappies));
        }
        if (numberOfSads === 0) {
          stringfyNumSad = "NONE";
        } else {
          stringfyNumSad = this.digitToWord(parseInt(numberOfSads));
        }

        return [stringfyNumHappy, stringfyNumSad];
      }
    },
    extractDissatisfiedsBinary(restId) {
      if (Object.keys(this.attractiveness).length > 0) {
        var sadnessBinary = this.extractDissatisfiedsAbsolutNumbers(restId)[1];
        if (sadnessBinary === "NONE") {
          return false;
        } else {
          return true;
        }
      } else {
        return false;
      }
    },
    digitToWord(digit) {
      if (digit === 0) {
        return "NONE";
      } else if (digit === 1) {
        return "ONE";
      } else if (digit === 2) {
        return "TWO";
      } else if (digit === 3) {
        return "THREE";
      } else if (digit === 4) {
        return "FOUR";
      } else {
        return "FIVE";
      }
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
    minDistance() {
      var min = 100000000000;
      for (var item of Object.values(this.membersDistance)) {
        if (item < min) {
          min = item;
        }
      }
      return min * 1000 - 1;
    },
    distance(rest) {
      var old_distance = 0;

      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Distance critice added",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      var newPreference = {};
      if (rest.price_expensive) {
        newPreference = {
          // distance: this.avrDistance() * 1000 - 1, Average dist
          distance: this.minDistance() - 0.1,
        };
      } else if (rest.price_mid) {
        newPreference = {
          // distance: this.avrDistance() * 1000 - 1,
          distance: this.minDistance() - 0.1,
        };
      } else {
        newPreference = {
          // distance: this.avrDistance() * 1000 - 1,
          distance: this.minDistance() - 0.1,
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

              if (
                (this.restaurantJsonRel.length < 1) &
                (this.restaurantJson.length < 1)
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
      this.priceDialog = ref(false);
      if (range === "rem") {
        var rangeSend = "";
      } else {
        var rangeSend = range;
      }
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Pice " + String(range) + "added",
      };
      this.$emit("critiqueIssued", rangeSend);
      sessionStorage.setItem("relevanceValidation", false);
      sessionStorage.setItem("attractivenessValidation", false);
      sessionStorage.setItem("SimilarityValidation", false);
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      var newPreference = {};
      if (range === "rem") {
        newPreference = {
          price_eco: true,
          price_mid: true,
          price_expensive: true,
        };
      } else if (range === "eco") {
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
          this.restPageActive = false;
        });
      this.mounting();
    },
    avergeAttr() {
      for (var rest of this.restaurantJsonRel) {
        var sum = 0;
        var count = 0;
        for (var userId of Object.keys(this.groupInfo)) {
          if (typeof this.attractiveness[userId] !== "undefined") {
            count++;
            sum = sum + this.attractiveness[userId][JSON.parse(rest).id];
          }
        }
        if (count > 0) {
          this.avrAttract[JSON.parse(rest).id] = sum / count;
          this.averAttrModleFunc(JSON.parse(rest).id, sum / count);
          this.fairnessModelFunc(JSON.parse(rest).id);
        } else {
          this.avrAttract[JSON.parse(rest).id] = sum;
          this.averAttrModleFunc(JSON.parse(rest).id, sum);
          this.fairnessModelFunc(JSON.parse(rest).id);
        }
      }
    },
    averAttrModleFunc(resturant, result) {
      if (result <= 0.0) {
        this.avrAttractModel[resturant] = ref(0);
      } else if (result <= 0.5) {
        this.avrAttractModel[resturant] = ref(0.5);
      } else if (result <= 1) {
        this.avrAttractModel[resturant] = ref(1);
      } else if (result <= 1.5) {
        this.avrAttractModel[resturant] = ref(1.5);
      } else if (result <= 2) {
        this.avrAttractModel[resturant] = ref(2);
      } else if (result <= 2.5) {
        this.avrAttractModel[resturant] = ref(2.5);
      } else if (result <= 3) {
        this.avrAttractModel[resturant] = ref(3);
      } else if (result <= 3.5) {
        this.avrAttractModel[resturant] = ref(3.5);
      } else if (result <= 4) {
        this.avrAttractModel[resturant] = ref(4);
      } else if (result <= 4.5) {
        this.avrAttractModel[resturant] = ref(4.5);
      } else {
        this.avrAttractModel[resturant] = ref(5);
      }
    },
    fairnessModelFunc(resturant) {
      var fairnessValue = this.extractDissatisfieds(resturant);
      if (fairnessValue <= 0) {
        this.fairModel[resturant] = ref(0);
      } else if (fairnessValue <= 0.1) {
        this.fairModel[resturant] = ref(0.5);
      } else if (fairnessValue <= 0.2) {
        this.fairModel[resturant] = ref(1);
      } else if (fairnessValue <= 0.3) {
        this.fairModel[resturant] = ref(1.5);
      } else if (fairnessValue <= 0.4) {
        this.fairModel[resturant] = ref(2);
      } else if (fairnessValue <= 0.5) {
        this.fairModel[resturant] = ref(2.5);
      } else if (fairnessValue <= 0.6) {
        this.fairModel[resturant] = ref(3);
      } else if (fairnessValue < 0.7) {
        this.fairModel[resturant] = ref(3.5);
      } else if (fairnessValue <= 0.8) {
        this.fairModel[resturant] = ref(4);
      } else if (fairnessValue < 0.9) {
        this.fairModel[resturant] = ref(4.5);
      } else {
        this.fairModel[resturant] = ref(5);
      }
    },
    similarityModelFunc(resturant, result) {
      if (result <= 0) {
        this.similarityModel[resturant] = ref(0);
      } else if (result <= 0.1) {
        this.similarityModel[resturant] = ref(0.5);
      } else if (result <= 0.2) {
        this.similarityModel[resturant] = ref(1);
      } else if (result <= 0.3) {
        this.similarityModel[resturant] = ref(1.5);
      } else if (result <= 0.4) {
        this.similarityModel[resturant] = ref(2);
      } else if (result <= 0.5) {
        this.similarityModel[resturant] = ref(2.5);
      } else if (result <= 0.6) {
        this.similarityModel[resturant] = ref(3);
      } else if (result <= 0.7) {
        this.similarityModel[resturant] = ref(3.5);
      } else if (result <= 0.8) {
        this.similarityModel[resturant] = ref(4);
      } else if (result <= 0.9) {
        this.similarityModel[resturant] = ref(4.5);
      } else {
        this.similarityModel[resturant] = ref(5);
      }
    },
    attractivenessModelFunc() {
      this.attractivenessModel = {};
      for (var userId of Object.keys(this.attractiveness)) {
        var userObject = {};
        for (var [key, value] of Object.entries(this.attractiveness[userId])) {
          if (value <= 0) {
            userObject[key] = ref(0);
          } else if (value <= 0.5) {
            userObject[key] = ref(0.5);
          } else if (value <= 1) {
            userObject[key] = ref(1);
          } else if (value <= 1.5) {
            userObject[key] = ref(1.5);
          } else if (value <= 2) {
            userObject[key] = ref(2);
          } else if (value <= 2.5) {
            userObject[key] = ref(2.5);
          } else if (value <= 3) {
            userObject[key] = ref(3);
          } else if (value <= 3.5) {
            userObject[key] = ref(3.5);
          } else if (value <= 4) {
            userObject[key] = ref(4);
          } else if (value <= 4.5) {
            userObject[key] = ref(4.5);
          } else {
            userObject[key] = ref(5);
          }
        }
        this.attractivenessModel[userId] = userObject;
      }
    },
    mounting() {
      this.pageload = false;
      var countMenu = 0;
      // sessionStorage.setItem("sorting", 4);
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
        this.restaurantJsonRel = this.restaurantJson;
        if (String(sessionStorage.getItem("menuSizeValidity")) !== "true") {
          for (var restident in Object.keys(this.restaurantJsonRel)) {
            countMenu++;
            this.menuSize(
              JSON.parse(this.restaurantJsonRel[restident]).id,
              countMenu
            );
          }
        } else {
          this.menuSizeRest = JSON.parse(sessionStorage.getItem("MenuSize"));
          this.menuSizeValidity = true;
        }
        this.populairtyModelFunc();
        this.RecomActive = true;
        // sessionStorage.setItem("sorting", -1);
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
            if (
              JSON.parse(sessionStorage.getItem("popularityValidation")) !==
              true
            ) {
              this.popularity(JSON.parse(resturant).id);
            } else {
              this.popularityObj = JSON.parse(
                sessionStorage.getItem("popularityObj")
              );
            }
            if (
              JSON.parse(
                sessionStorage.getItem("selectedPopularityValidation")
              ) !== true
            ) {
              this.selectedPopularity(JSON.parse(resturant).id);
            } else {
              this.selectedPopularityObj = JSON.parse(
                sessionStorage.getItem("selectedPopularity")
              );
            }
          }
          this.pageloadbooked = true;
          sessionStorage.setItem("popularityValidation", true);

          sessionStorage.setItem("selectedPopularityValidation", true);
        });
        url =
          "http://46.18.25.97:8050/recommendations/relevance/" + grouIdTested;
        if (
          JSON.parse(sessionStorage.getItem("relevanceValidation")) !== true
        ) {
          axios.get(url).then((response) => {
            if (JSON.parse(JSON.stringify(response.data)).length > 0) {
              this.restaurantJsonRel = JSON.parse(
                JSON.stringify(response.data)
              );
              sessionStorage.setItem(
                "relevance",
                JSON.stringify(this.restaurantJsonRel)
              );
              sessionStorage.setItem("relevanceValidation", true);

              this.restaurantJsonRelOrignal = this.restaurantJsonRel;
              this.restaurantJsonRelActive = true;
              this.RecomActive = true;
              if (this.RecomActive) {
                if (
                  JSON.parse(sessionStorage.getItem("SimilarityValidation")) ===
                  true
                ) {
                  this.similarityValue = JSON.parse(
                    sessionStorage.getItem("SimilarityValue")
                  );
                  for (const [key, value] of Object.entries(
                    this.similarityValue
                  )) {
                    this.similarityModelFunc(key, value);
                  }
                } else {
                  this.similarityValidity = false;
                  var countSimilar = 0;
                  for (var restident in Object.keys(this.restaurantJsonRel)) {
                    countSimilar++;
                    this.getSimilarity(
                      JSON.parse(this.restaurantJsonRel[restident]).id,
                      countSimilar
                    );
                  }
                }
              }
              const urlAttract =
                "http://46.18.25.97:8050/recommendations/attractiveness/" +
                grouIdTested;
              if (
                JSON.parse(
                  sessionStorage.getItem("attractivenessValidation")
                ) !== true
              ) {
                axios.get(urlAttract).then((response) => {
                  this.attractiveness = JSON.parse(
                    JSON.stringify(response.data)
                  );
                  this.attractivenessModelFunc();
                  this.bannerValidation(this.restaurantJsonRel);
                  sessionStorage.setItem(
                    "attractiveness",
                    JSON.stringify(this.attractiveness)
                  );
                  sessionStorage.setItem("attractivenessValidation", true);
                  var organizer_id = Object.keys(this.groupInfo)[0];
                  this.organizer_user_attractiveness =
                    this.attractiveness[organizer_id];
                  if (this.RecomActive) {
                    if (parseInt(sessionStorage.getItem("sorting")) !== -2) {
                      this.sorting(
                        parseInt(sessionStorage.getItem("sorting")),
                        0,
                        0
                      );
                      this.fairness_attractiveness();
                    } else {
                      this.sorting(-1, 0, 0);
                      this.fairness_attractiveness();
                    }
                  }
                  this.pageload = true;
                  this.avergeAttr();
                });
              } else {
                this.attractiveness = JSON.parse(
                  sessionStorage.getItem("attractiveness")
                );
                this.attractivenessModelFunc();
                this.bannerValidation(this.restaurantJsonRel);
                var organizer_id = Object.keys(this.groupInfo)[0];
                this.organizer_user_attractiveness =
                  this.attractiveness[organizer_id];
                if (this.RecomActive) {
                  if (parseInt(sessionStorage.getItem("sorting")) !== -2) {
                    this.sorting(
                      parseInt(sessionStorage.getItem("sorting")),
                      0,
                      0
                    );
                    this.fairness_attractiveness();
                  } else {
                    this.sorting(-1, 0, 0);
                    this.fairness_attractiveness();
                  }
                }
                this.pageload = true;
                this.avergeAttr();
              }
            } else {
              this.sorting(parseInt(-1, 0, 0));
              this.pageload = true;
            }
          });
        } else {
          if (JSON.parse(JSON.stringify(response.data)).length > 0) {
            this.restaurantJsonRel = JSON.parse(
              sessionStorage.getItem("relevance")
            );
            if (this.RecomActive) {
              if (
                JSON.parse(sessionStorage.getItem("SimilarityValidation")) ===
                true
              ) {
                this.similarityValue = JSON.parse(
                  sessionStorage.getItem("SimilarityValue")
                );
                for (const [key, value] of Object.entries(
                  this.similarityValue
                )) {
                  this.similarityModelFunc(key, value);
                }
              } else {
                this.similarityValidity = false;
                for (var restident in Object.keys(this.restaurantJsonRel)) {
                  this.getSimilarity(
                    JSON.parse(this.restaurantJsonRel[restident]).id,
                    this.restaurantJsonRel.length
                  );
                }
              }
            }
            this.restaurantJsonRelOrignal = this.restaurantJsonRel;
            this.restaurantJsonRelActive = true;
            this.RecomActive = true;
            const urlAttract =
              "http://46.18.25.97:8050/recommendations/attractiveness/" +
              grouIdTested;
            if (
              JSON.parse(sessionStorage.getItem("attractivenessValidation")) !==
              true
            ) {
              axios.get(urlAttract).then((response) => {
                this.attractiveness = JSON.parse(JSON.stringify(response.data));
                this.attractivenessModelFunc();
                this.bannerValidation(this.restaurantJsonRel);
                sessionStorage.setItem(
                  "attractiveness",
                  JSON.stringify(this.attractiveness)
                );
                sessionStorage.setItem("attractivenessValidation", true);
                var organizer_id = Object.keys(this.groupInfo)[0];
                this.organizer_user_attractiveness =
                  this.attractiveness[organizer_id];
                if (this.RecomActive) {
                  if (parseInt(sessionStorage.getItem("sorting")) !== -2) {
                    this.sorting(
                      parseInt(sessionStorage.getItem("sorting")),
                      0,
                      0
                    );
                    this.fairness_attractiveness();
                  } else {
                    this.sorting(-1, 0, 0);
                    this.fairness_attractiveness();
                  }
                }
                this.pageload = true;
                this.avergeAttr();
              });
            } else {
              this.attractiveness = JSON.parse(
                sessionStorage.getItem("attractiveness")
              );
              this.attractivenessModelFunc();
              this.bannerValidation(this.restaurantJsonRel);
              var organizer_id = Object.keys(this.groupInfo)[0];
              this.organizer_user_attractiveness =
                this.attractiveness[organizer_id];
              if (this.RecomActive) {
                if (parseInt(sessionStorage.getItem("sorting")) !== -2) {
                  this.sorting(
                    parseInt(sessionStorage.getItem("sorting")),
                    0,
                    0
                  );
                  this.fairness_attractiveness();
                } else {
                  this.sorting(-1, 0, 0);
                  this.fairness_attractiveness();
                }
              }
              this.pageload = true;
              this.avergeAttr();
            }
          } else {
            this.sorting(-1, 0, 0);
            this.pageload = true;
          }
        }
      });
    },
  },
  mounted() {
    const url = "http://46.18.25.97:8050/recommendations/get/popularity/count";
    axios.get(url).then((response) => {
      this.countPopularity = response.data;
      this.mounting();
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
  margin-bottom: 0px;
}
.button-back {
  margin-top: 5px;
  margin-left: 5px;
  position: fixed;
  z-index: 30;
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
.card-styling {
  padding-top: 2px;
  padding-bottom: 2px;
}
.float-parent-element {
  width: 100%;
}
.float-child-element {
  float: left;
  width: 100%;
}
.descript {
}
.sadnessActive {
  width: 100%;
  height: 150px;
  padding: 5px;
  border-color: red;
  height: auto;
}
.sadnessNotActive {
  width: 100%;
  height: 150px;
  padding: 5px;
  border-color: green;
  height: auto;
}
.emotion {
  border-radius: 50%;
}
.memberExplan {
  padding-left: 0px;
  padding-right: 0px;
}
.q-chip {
  cursor: default;
}
.container {
  overflow: hidden;
}
.left {
  float: left;
  width: auto;
}
.right {
  float: right;
  width: auto;
}
.center {
  float: left;
  margin-left: 16px;
}
</style>
