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
          <!-- Uncomment this and chenge the above OK to CANCEK -->
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
                similarityValue[bookedRestId]
              )
            "
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  <q-dialog v-model="scoreDialog">
    <q-card>
      <q-card-section>
        <div v-if="scoreExplanation === 'sug'" class="text-h6">
          Suggested by App
        </div>
      </q-card-section>
      <q-card-section class="q-pt-none" align="justify">
        <div v-if="scoreExplanation === 'sug'">
          Based on the group's overall satisfaction, the restaurant's popularity
          in our application, and the menu diversity with respect to the group
          members' preferences, this restaurant is suggested as the best choice
          for your group.
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <!-- <div v-if="pageLoad && selectionLoad"> -->
  <div v-if="bookmarkedLength !== 0">
    <div>
      <div
        v-if="userPreferenceList.length > 0"
        class="row no-wrap"
        style="overflow-y: auto"
      >
        <!-- <div style="width: 100%">
          <div class="row no-wrap">
            <div
              v-if="critiqueRange !== '' && restPageActive  === false"
              @click="openPriceCritique()"
            >
              <q-chip square color="blue" text-color="white">
                {{ getRange() }}
              </q-chip>
            </div>
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
          </div>
          <q-separator />
        </div> -->
      </div>
      <div v-else>
        <div class="row no-wrap">
          <div
            v-if="critiqueRange !== '' && restPageActive === false"
            @click="openPriceCritique()"
          >
            {{ scrollToTop() }}
            <q-chip
              icon="price_change"
              square
              color="primary"
              text-color="white"
            >
              {{ getRange() }}
            </q-chip>
          </div>
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
          <q-separator />
        </div>
        <q-separator />
      </div>
      <div
        v-if="
          selectionLoad &&
          pageLoaded &&
          pageLoadedSimilarity &&
          pageLoadedAll &&
          popularityModelLoad &&
          similarityValidity &&
          menuSizeValidity
        "
      >
        <div v-if="restPageActive">
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
              padding-top: 20px;
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
                  @click="restPageActive = !restPageActive"
                />
              </div>
              <div class="parent">
                <strong>{{ restuaurants[navigated[0]].name }}</strong>
              </div>
            </div>
          </div>
          <!-- <q-btn
            round
            color="primary"
            icon="chevron_left"
            position="top-left"
            @click="restPageActive = !restPageActive"
            size="0.7em"
            class="button-back"
          /> -->
          <div
            v-for="bookedId in navigated"
            :key="bookedId"
            style="width: 100%"
          >
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
                      padding: 3px 0px 3px 0px;
                    "
                  >
                    <q-img
                      :src="getLogoIn(restuaurants[bookedId].logo)"
                      style="max-width: 100%; height: 200px"
                    />
                  </div>
                  <q-separator style="margin: 3px 0px 3px 0px" />
                </q-card-section>
                <q-card-section class="card-styling">
                  <div class="row no-wrap items-center" style="padding: 3px">
                    <strong>{{ restuaurants[bookedId].name }}</strong>
                  </div>
                  <div v-if="scoreExplanation === 'sug'">
                    <div><strong>Suggested by App</strong></div>
                  </div>
                  <div v-if="scoreExplanation === 'pop'">
                    <div>This resturant popularity in our app</div>
                    <q-rating
                      v-model="popularityModel[restuaurants[bookedId].id]"
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
                      v-model="tripScore[restuaurants[bookedId].id]"
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
                        (menuSizeRest[restuaurants[bookedId].id]["dishes"] /
                          100) *
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
                        (menuSizeRest[restuaurants[bookedId].id]["category"] /
                          10) *
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
                  <div v-if="scoreExplanation === 'avrattr'">
                    <div>
                      The overall fitness of this restaurant for your group
                    </div>
                    <q-rating
                      v-model="avrAttractModel[restuaurants[bookedId].id]"
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
                  <div v-if="scoreExplanation === 'sim'">
                    <div>Popularity among groups with your preferences</div>
                    <q-rating
                      v-model="similarityModel[restuaurants[bookedId].id]"
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
                      v-model="fairModel[restuaurants[bookedId].id]"
                      size="1.5em"
                      :max="5"
                      color="orange"
                      readonly
                      icon="star_border"
                      icon-selected="star"
                      icon-half="star_half"
                      no-dimming
                    ></q-rating>
                  </div>
                  <q-separator style="margin: 8px 0px 0px 0px" />
                  <div
                    v-if="scoreExplanation === 'avrattr'"
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
                    v-if="scoreExplanation === 'sim'"
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
                  <div v-if="scoreExplanation === 'trip'">
                    For more information visit the restaurant's
                    <a
                      :href="tripPage[restuaurants[bookedId].id]"
                      style="text-decoration: none"
                      target="_blank"
                      ><b>TripAdvisor Page</b></a
                    >
                  </div>
                  <div v-if="scoreExplanation === 'dishDiv'">
                    There are
                    {{ menuSizeRest[restuaurants[bookedId].id]["dishes"] }}
                    types of dishes in the menu of this restaurant.
                  </div>
                  <div v-if="scoreExplanation === 'categ'">
                    There are
                    {{ menuSizeRest[restuaurants[bookedId].id]["category"] }}
                    category of dishes in the menu of this restaurant.
                  </div>
                </q-card-section>
                <div v-if="scoreExplanation === 'sug'">
                  <q-card-section class="q-pt-none" align="justify">
                    Based on the group's overall satisfaction, the restaurant's
                    popularity in our application, and the menu diversity with
                    respect to the group members' preferences, this restaurant
                    is suggested as the best choice for your group.
                  </q-card-section>
                </div>
                <q-card-section class="q-pt-none" align="justify">
                  <div
                    v-if="scoreExplanation === 'avrattr'"
                    style="margin: 8px 0px 0px 0px"
                  >
                    Satisfaction level for
                    <div
                      v-for="(
                        userAttractiveness, name, index
                      ) in attractiveness"
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
                                attractivenessModel[name][
                                  restuaurants[bookedId].id
                                ]
                              "
                              size="1.5em"
                              :max="5"
                              :color="
                                groupInfo[name][0] === 'Organizer'
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
                                  groupInfo[name][1]
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
                          restuaurants[bookedId].id
                        )[1] === 'NONE'
                      "
                    >
                      All of your group members are satisfied.
                    </div>
                    <div v-else>
                      <div
                        v-if="
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
                          )[0] !== 'NONE'
                        "
                      >
                        {{
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
                          )[0]
                        }}
                        of your group members
                        {{
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
                          )[0] === "NONE" ||
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
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
                          restuaurants[bookedId].id
                        )[1] !== 'NONE'
                      "
                    >
                      <div
                        v-if="
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
                          )[0] === 'NONE'
                        "
                      >
                        All of you group members are not satisfied.
                      </div>
                      <div v-else>
                        {{
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
                          )[1]
                        }}
                        of your group members
                        {{
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
                          )[1] === "NONE" ||
                          extractDissatisfiedsAbsolutNumbers(
                            restuaurants[bookedId].id
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
                          restuaurants[bookedId].id
                        )[1] !== 'NONE' &&
                        extractDissatisfiedsAbsolutNumbers(
                          restuaurants[bookedId].id
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
                          restuaurants[bookedId].id
                        )[1] !== 'NONE' &&
                        extractDissatisfiedsAbsolutNumbers(
                          restuaurants[bookedId].id
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
                  <div v-if="scoreExplanation === 'sim'">
                    <br />
                    <div v-html="this.similarityExplanation"></div>
                    <div
                      v-for="(
                        userAttractiveness, name, index
                      ) in attractiveness"
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
                                  restuaurants[bookedId].id
                                )
                              }}
                            </p>
                          </q-item-label>
                        </q-item-section>
                      </q-item>
                    </div>
                  </div>
                  <div v-if="scoreExplanation === 'pop'">
                    <div
                      v-if="popPercentage(restuaurants[bookedId].id) === '100'"
                    >
                      This restaurant is the <strong>most</strong> popular
                      restaurant in our application.
                    </div>
                    <div v-else>
                      This restaurant is more popular than
                      <strong
                        >{{ popPercentage(restuaurants[bookedId].id) }}%</strong
                      >
                      of the restaurants in our application.
                    </div>
                  </div>
                </q-card-section>
                <q-card-actions align="right">
                  <q-btn flat label="OK" color="primary" v-close-popup />
                </q-card-actions>
              </q-card>
            </q-dialog>
            <div
              class="card-position q-pa-md row items-start q-gutter-md"
              style="padding-left: 1px; padding-right: 1px"
            >
              <div
                v-if="extractDissatisfiedsBinary(restuaurants[bookedId].id)"
                style="width: 100%"
              >
                <q-card
                  class="my-card"
                  style="
                    width: 100%;
                    margin: auto;
                    border-color: red;
                    margin-top: 35px;
                  "
                  flat
                  bordered
                >
                  <img
                    :src="getLogo(restuaurants[bookedId].logo)"
                    style="height: 200px; padding: 2px; border-radius: 5px"
                  />
                  <div
                    class="absolute"
                    style="top: 4px; left: 4px; border-radius: 25px"
                  >
                    <div class="q-pa-md" style="padding: 5px">
                      <div class="q-gutter-y-md column">
                        <q-rating
                          v-model="model3"
                          max="1"
                          size="25px"
                          color="red-9"
                          color-selected="red-9"
                          icon="favorite_border"
                          icon-selected="favorite"
                          @click="
                            submitRemoveBookmark(restuaurants[bookedId].id)
                          "
                          style="background: white; border-radius: 3px"
                        />
                      </div>
                    </div>
                  </div>
                  <div
                    class="absolute"
                    style="
                      top: 190px;
                      left: 7px;
                      /* transform: translateX(-90%);
                          transform: translateY(-95%); */
                    "
                  >
                    {{
                      suggestionEvaluation(
                        fariness(bookedId),
                        attractiveness,
                        bookedId
                      )
                    }}
                    <div
                      v-if="suggestionObj[bookedId] >= maxSuggestion"
                      style="margin: 1px; color: green"
                    >
                      <q-btn
                        icon="offline_pin"
                        color="green"
                        size="10px"
                        style="width: 65px; opacity: 0.8"
                        @click="scoreDialogFunc('sug', bookedId)"
                        >Suggested by app</q-btn
                      >
                    </div>
                  </div>
                  <q-card-section
                    class="q-pt-none"
                    style="
                      width: 100%;
                      padding-left: 1px;
                      padding-right: 1px;
                      margin-top: 0px;
                      margin-bottom: 0px;
                    "
                  >
                    <div
                      class="q-pa-md row items-start q-gutter-md"
                      style="width: 100%; padding-right: 0px"
                    >
                      <q-card class="my-card" style="width: 100%">
                        <q-card-section
                          style="margin-top: 0px; margin-bottom: 0px"
                        >
                          <div
                            class="card-styling"
                            style="
                              margin-top: 0px;
                              margin-bottom: 0px;
                              padding-left: 16px;
                              padding-right: 16px;
                            "
                          >
                            <div v-if="selectedRest === bookedId">
                              <p style="color: green">
                                You have selected this restaurant. You may
                                change your choice by selecting another
                                restaurant.
                              </p>
                            </div>
                            <div class="text-h6 q-mb-xs">
                              <p
                                style="padding-bottom: 8px; margin-bottom: 0px"
                              >
                                {{ restuaurants[bookedId].name }}
                              </p>
                            </div>
                            <p style="padding-bottom: 8px; margin-bottom: 0px">
                              Address: {{ restuaurants[bookedId].address }},
                              {{ restuaurants[bookedId].city }}, Italy
                            </p>
                            <p style="padding-bottom: 8px; margin-bottom: 0px">
                              <a
                                :href="links[restuaurants[bookedId].name]"
                                style="text-decoration: none; cursor: pointer"
                                target="_blank"
                                ><b>Restaurant Page</b></a
                              >
                            </p>
                            <q-list
                              v-if="
                                extractDissatisfiedsBinary(
                                  restuaurants[bookedId].id
                                ) && restaurantJsonRel.length
                              "
                              dense
                              style="padding-bottom: 8px; margin-bottom: 0px"
                            >
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
                                    color="yellow"
                                    size="xs"
                                  />
                                </q-item-section>
                                <q-item-section
                                  style="margin-left: -20px; padding-right: 0px"
                                  dense
                                >
                                  {{ sadsList[restuaurants[bookedId].id] }}
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <q-list
                              v-else
                              style="padding-bottom: 8px; margin-bottom: 0px"
                            >
                              <q-item
                                style="padding-left: 0px; padding-right: 8px"
                                dense
                              >
                                <q-item-section avatar dense>
                                  <q-icon
                                    name="offline_pin"
                                    color="green"
                                    size="xs"
                                  />
                                </q-item-section>
                                <q-item-section
                                  style="margin-left: -20px; padding-right: 0px"
                                  >All members will be satisfied with this
                                  restaurant.
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <q-separator />
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
                                  icon="restaurant_menu"
                                  label="Menu"
                                  caption="Menu List"
                                >
                                  <div
                                    v-for="(
                                      foodList, category, index
                                    ) in menuList"
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
                                              <q-item-section>{{
                                                food
                                              }}</q-item-section>
                                            </q-item>
                                          </q-list>
                                          <q-separator />
                                        </div>
                                      </div>
                                    </q-expansion-item>
                                  </div>
                                </q-expansion-item>
                              </q-list>
                            </div>
                            <q-separator style="margin-bottom: 10px" />
                            <p
                              v-show="Boolean(restuaurants[bookedId].price_eco)"
                              style="margin-bottom: 8px"
                            >
                              Restaurant price is <strong>economic</strong>. Do
                              you prefer to change the price range to mid-range
                              or expensive?
                            </p>
                            <div
                              class="parent"
                              v-show="Boolean(restuaurants[bookedId].price_eco)"
                            >
                              <!-- <q-btn
                              color="grey"
                              label="$"
                              class="critique-btn"
                            /> -->
                              <q-btn
                                color="primary"
                                icon="price_change"
                                label="Mid-range"
                                @click="price('mid')"
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
                              v-show="Boolean(restuaurants[bookedId].price_mid)"
                              style="margin-bottom: 8px"
                            >
                              Restaurant price is <strong>mid-range</strong>. Do
                              you prefer to change the price range to economical
                              or expensive?
                            </p>
                            <div
                              class="parent"
                              v-show="Boolean(restuaurants[bookedId].price_mid)"
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
                                Boolean(restuaurants[bookedId].price_expensive)
                              "
                              style="margin-bottom: 8px"
                            >
                              Restaurant price is <strong>expensive</strong>. Do
                              you prefer to change the price range to economical
                              or mid-range?
                            </p>
                            <div
                              class="parent"
                              v-show="
                                Boolean(restuaurants[bookedId].price_expensive)
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

                          <div class="card-styling">
                            <!-- <div
                              v-if="sortingType === 'pop'"
                              style="
                                display: inline;
                                width: 100%;
                                margin-bottom: 8px;
                                padding-bottom: 4px;
                              "
                            >
                              Popularity
                              <q-icon
                                size="xxs"
                                name="info"
                                color="primary"
                                @click="
                                  scoreDialogFunc(
                                    'pop',
                                    restuaurants[bookedId].id
                                  )
                                "
                              />:
                              <q-rating
                                v-model="
                                  popularityModel[restuaurants[bookedId].id]
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
                            </div> -->
                            <!-- <div v-if="sortingType === 'avrattr'">
                              Fitness for your group:
                              <q-icon
                                size="xxs"
                                name="info"
                                color="primary"
                                @click="
                                  scoreDialogFunc(
                                    'avrattr',
                                    restuaurants[bookedId].id
                                  )
                                "
                              />
                              <q-rating
                                v-model="
                                  avrAttractModel[restuaurants[bookedId].id]
                                "
                                size="1.5em"
                                :max="5"
                                color="orange"
                                readonly
                                icon="star_border"
                                icon-selected="star"
                                icon-half="star_half"
                              ></q-rating> -->
                            <!-- <q-linear-progress
                              :value="avrAttract[restuaurants[bookedId].id]"
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
                                    parseFloat(
                                      avrAttract[restuaurants[bookedId].id]
                                    ).toFixed(2) *
                                      100 +
                                    '%'
                                  "
                                />
                              </div>
                            </q-linear-progress> -->
                            <!-- </div> -->
                            <!-- <div v-if="sortingType === 'attr'">
                            Attractiveness for
                            {{
                              groupInfo[sortUserId][1] === "Organizer"
                                ? "you"
                                : groupInfo[sortUserId][1]
                            }}:
                            <q-linear-progress
                              :value="
                                attractiveness[sortUserId][
                                  restuaurants[bookedId].id
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
                                          restuaurants[bookedId].id
                                        ]
                                      ).toFixed(2) * 100
                                    ) + '%'
                                  "
                                />
                              </div>
                            </q-linear-progress>
                          </div> -->
                            <!-- <div v-if="sortingType === 'fair'">
                              Group satisfaction equality
                              <q-icon
                                size="xxs"
                                name="info"
                                color="primary"
                                @click="
                                  scoreDialogFunc(
                                    'fair',
                                    restuaurants[bookedId].id
                                  )
                                "
                              />:&nbsp;&nbsp;&nbsp; -->
                            <!-- <q-linear-progress
                              :value="fariness(restuaurants[bookedId].id)"
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
                                        fariness(restuaurants[bookedId].id)
                                      ).toFixed(2) * 100
                                    ) + '%'
                                  "
                                />
                              </div>
                            </q-linear-progress> -->
                            <!-- <q-rating
                                v-model="fairModel[restuaurants[bookedId].id]"
                                size="1.5em"
                                :max="5"
                                color="orange"
                                icon-selected="img:https://img.icons8.com/ios/100/FD7E14/anime-emoji--v1.png"
                                icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                                readonly
                              ></q-rating>
                            </div> -->
                            <!-- <div v-if="sortingType === 'attrfair'">
                            Fairness and attractiveness score:
                            <q-linear-progress
                              :value="fair_attract[restuaurants[bookedId].id]"
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
                                        fair_attract[restuaurants[bookedId].id]
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
                            <!-- </p> -->

                            <!-- <p style="margin-top: 6px; margin-bottom: 6px">
                                Similarity to groups who liked this restaurant
                                <q-icon
                                  size="xxs"
                                  name="info"
                                  color="primary"
                                  @click="
                                    scoreDialogFunc(
                                      'sim',
                                      restuaurants[bookedId].id
                                    )
                                  "
                                />:&nbsp;&nbsp;&nbsp; -->
                            <!-- <q-linear-progress
                              :value="
                                similarityValue[restuaurants[bookedId].id]
                              "
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
                                        restuaurants[bookedId].id
                                      ].toFixed(2) * 100
                                    ) + '%'
                                  "
                                />
                              </div>
                            </q-linear-progress> -->
                            <!-- <q-rating
                                  v-model="
                                    similarityModel[restuaurants[bookedId].id]
                                  "
                                  size="1.5em"
                                  :max="5"
                                  icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                                  icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                                  readonly
                                ></q-rating>
                              </p>
                            </div> -->

                            <!-- <q-list
                              class="rounded-borders"
                              style="padding: 0px"
                              v-if="sortingType !== 'pop'"
                            > -->
                            <!-- <q-expansion-item
                              expand-separator
                              icon="favorite_border"
                              label="Popularity"
                              @click="storeGeneralInteraction()"
                            > -->

                            <!-- <p>
                                Selected as the final choice:

                                <q-linear-progress
                                  :value="
                                    selectedPopularityObj[
                                      restuaurants[bookedId].id
                                    ]
                                  "
                                  color="teal-3"
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
                                          selectedPopularityObj[
                                            restuaurants[bookedId].id
                                          ].toFixed(2) * 100
                                        ) + '%'
                                      "
                                    />
                                  </div>
                                </q-linear-progress>
                              </p> -->
                            <!-- </q-expansion-item> -->
                            <q-separator
                              style="margin-top: 6px; margin-bottom: 6px"
                            />
                            <!-- </q-list> -->
                          </div>
                          <q-card-section>
                            <q-list class="rounded-borders">
                              <q-item>
                                <q-item-section>Popularity</q-item-section>
                                <q-item-section>
                                  <q-rating
                                    v-model="
                                      popularityModel[restuaurants[bookedId].id]
                                    "
                                    max="5"
                                    size="1.5em"
                                    color="red"
                                    color-selected="red-9"
                                    icon="favorite_border"
                                    icon-selected="favorite"
                                    icon-half="favorite"
                                    no-dimming
                                    readonly /></q-item-section
                                ><q-item-section avatar
                                  ><q-icon
                                    size="sm"
                                    name="info"
                                    color="primary"
                                    @click="scoreDialogFunc('pop')"
                                    style="cursor: pointer"
                                  />
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <div
                              v-if="restaurantJsonRel.length"
                              class="card-styling"
                            >
                              <q-list class="rounded-borders">
                                <q-item>
                                  <q-item-section
                                    >Fitness for your group</q-item-section
                                  >

                                  <q-item-section>
                                    <q-rating
                                      v-model="
                                        avrAttractModel[
                                          restuaurants[bookedId].id
                                        ]
                                      "
                                      max="5"
                                      size="1.5em"
                                      color="green"
                                      icon="star_border"
                                      icon-selected="star"
                                      icon-half="star_half"
                                      no-dimming
                                      readonly /></q-item-section
                                  ><q-item-section avatar
                                    ><q-icon
                                      size="sm"
                                      name="info"
                                      color="primary"
                                      @click="scoreDialogFunc('avrattr')"
                                      style="cursor: pointer"
                                    />
                                  </q-item-section>
                                </q-item>
                              </q-list>
                              <q-list class="rounded-borders">
                                <q-item>
                                  <q-item-section
                                    >Similarity to the group which bookmarked
                                    this restaurant</q-item-section
                                  >
                                  <q-item-section>
                                    <q-rating
                                      v-model="
                                        similarityModel[
                                          restuaurants[bookedId].id
                                        ]
                                      "
                                      size="1.5em"
                                      :max="5"
                                      icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                                      icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                                      readonly /></q-item-section
                                  ><q-item-section avatar
                                    ><q-icon
                                      size="sm"
                                      name="info"
                                      color="primary"
                                      @click="
                                        scoreDialogFunc(
                                          'sim',
                                          restuaurants[bookedId].id
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
                                    TripAdvisor score
                                  </q-item-section>
                                  <q-item-section dense>
                                    <q-rating
                                      v-model="
                                        tripScore[restuaurants[bookedId].id]
                                      "
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
                                          JSON.parse(restuaurants[bookedId]).id
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
                                          (menuSizeRest[
                                            restuaurants[bookedId].id
                                          ]["category"] /
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
                                          (menuSizeRest[
                                            restuaurants[bookedId].id
                                          ]["dishes"] /
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
                          </q-card-section>
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
                      <q-card-section
                        style="width: 100%; margin-top: 0px; margin-bottom: 0px"
                      >
                        {{ memberDistanceCal(restuaurants[bookedId].id) }}
                        <div v-for="(value, key) in groupInfo" :key="key">
                          {{ value[1] }}'s distance
                          {{ membersDistance[key] }} KM
                        </div>
                        <p></p>
                        <!-- Group's average distance
                  {{ avrDistance(restuaurants[bookedId]) }} KM
                  <p></p> -->
                        <div class="parent">
                          <q-btn
                            color="primary"
                            label="Closer"
                            @click="distance(restuaurants[bookedId])"
                          />
                        </div>
                      </q-card-section>
                    </q-card>
                  </q-card-section>
                </q-card>
              </div>
              <div v-else style="width: 100%">
                <q-card
                  class="my-card"
                  style="
                    width: 100%;
                    margin: auto;
                    border-color: green;
                    margin-top: 35px;
                  "
                  flat
                  bordered
                >
                  <img
                    :src="getLogo(restuaurants[bookedId].logo)"
                    style="height: 200px; padding: 2px; border-radius: 5px"
                  />
                  <div
                    class="absolute"
                    style="top: 4px; left: 4px; border-radius: 25px"
                  >
                    <div class="q-pa-md" style="padding: 5px">
                      <div class="q-gutter-y-md column">
                        <q-rating
                          v-model="model3"
                          max="1"
                          size="25px"
                          color="red-9"
                          color-selected="red-9"
                          icon="favorite_border"
                          icon-selected="favorite"
                          @click="
                            submitRemoveBookmark(restuaurants[bookedId].id)
                          "
                          style="background: white; border-radius: 3px"
                        />
                      </div>
                    </div>
                  </div>
                  <div
                    class="absolute"
                    style="
                      top: 190px;
                      left: 7px;
                      /* transform: translateX(-90%);
                          transform: translateY(-95%); */
                    "
                  >
                    {{
                      suggestionEvaluation(
                        fariness(bookedId),
                        attractiveness,
                        bookedId
                      )
                    }}
                    <div
                      v-if="suggestionObj[bookedId] >= maxSuggestion"
                      style="margin: 1px; color: green"
                    >
                      <q-btn
                        icon="offline_pin"
                        color="green"
                        size="10px"
                        style="width: 65px; opacity: 0.8"
                        @click="scoreDialogFunc('sug', bookedId)"
                        >Suggested by app</q-btn
                      >
                    </div>
                  </div>
                  <q-card-section
                    class="q-pt-none"
                    style="
                      width: 100%;
                      padding-left: 1px;
                      padding-right: 1px;
                      margin-top: 0px;
                      margin-bottom: 0px;
                    "
                  >
                    <div
                      class="q-pa-md row items-start q-gutter-md"
                      style="width: 100%; padding-right: 0px"
                    >
                      <q-card class="my-card" style="width: 100%">
                        <q-card-section
                          style="
                            margin-top: 0px;
                            margin-bottom: 0px;
                            padding-left: 16px;
                            padding-right: 16px;
                          "
                        >
                          <div
                            class="card-styling"
                            style="
                              margin-top: 0px;
                              margin-bottom: 0px;
                              padding-left: 16px;
                              padding-right: 16px;
                            "
                          >
                            <div v-if="selectedRest === bookedId">
                              <p style="color: green">
                                You have selected this restaurant. You may
                                change your choice by selecting another
                                restaurant.
                              </p>
                            </div>
                            <div class="text-h6 q-mb-xs">
                              <p
                                style="padding-bottom: 8px; margin-bottom: 0px"
                              >
                                {{ restuaurants[bookedId].name }}
                              </p>
                            </div>
                            <p style="padding-bottom: 8px; margin-bottom: 0px">
                              Address: {{ restuaurants[bookedId].address }},
                              {{ restuaurants[bookedId].city }}, Italy
                            </p>
                            <p style="padding-bottom: 8px; margin-bottom: 0px">
                              <a
                                :href="links[restuaurants[bookedId].name]"
                                style="text-decoration: none; cursor: pointer"
                                target="_blank"
                                ><b>Restaurant Page</b></a
                              >
                            </p>
                            <q-list
                              v-if="
                                extractDissatisfiedsBinary(
                                  restuaurants[bookedId].id
                                ) && restaurantJsonRel.length
                              "
                              dense
                              style="padding-bottom: 8px; margin-bottom: 0px"
                            >
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
                                    color="yellow"
                                    size="xs"
                                  />
                                </q-item-section>
                                <q-item-section
                                  style="margin-left: -20px; padding-right: 0px"
                                  dense
                                >
                                  {{ sadsList[restuaurants[bookedId].id] }}
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <q-list
                              v-else
                              style="padding-bottom: 8px; margin-bottom: 0px"
                            >
                              <q-item
                                style="padding-left: 0px; padding-right: 8px"
                                dense
                              >
                                <q-item-section avatar dense>
                                  <q-icon
                                    name="offline_pin"
                                    color="green"
                                    size="xs"
                                  />
                                </q-item-section>
                                <q-item-section
                                  style="margin-left: -20px; padding-right: 0px"
                                  >All members will be satisfied with this
                                  restaurant.
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <q-separator />
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
                                  icon="restaurant_menu"
                                  label="Menu"
                                  caption="Menu List"
                                >
                                  <div
                                    v-for="(
                                      foodList, category, index
                                    ) in menuList"
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
                                          <q-separator />
                                        </div>
                                      </div>
                                    </q-expansion-item>
                                  </div>
                                </q-expansion-item>
                              </q-list>
                            </div>
                            <q-separator style="margin-bottom: 10px" />
                            <p
                              v-show="Boolean(restuaurants[bookedId].price_eco)"
                              style="margin-bottom: 8px"
                            >
                              Restaurant price is <strong>economic</strong>. Do
                              you prefer to change the price range to mid-range
                              or expensive?
                            </p>
                            <div
                              class="parent"
                              v-show="Boolean(restuaurants[bookedId].price_eco)"
                            >
                              <!-- <q-btn
                              color="grey"
                              label="$"
                              class="critique-btn"
                            /> -->
                              <q-btn
                                color="primary"
                                icon="price_change"
                                label="Mid-range"
                                @click="price('mid')"
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
                              v-show="Boolean(restuaurants[bookedId].price_mid)"
                              style="margin-bottom: 8px"
                            >
                              Restaurant price is <strong>mid-range</strong>. Do
                              you prefer to change the price range to economical
                              or expensive?
                            </p>
                            <div
                              class="parent"
                              v-show="Boolean(restuaurants[bookedId].price_mid)"
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
                                Boolean(restuaurants[bookedId].price_expensive)
                              "
                              style="margin-bottom: 8px"
                            >
                              Restaurant price is <strong>expensive</strong>. Do
                              you prefer to change the price range to economical
                              or mid-range?
                            </p>
                            <div
                              class="parent"
                              v-show="
                                Boolean(restuaurants[bookedId].price_expensive)
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
                        </q-card-section>
                        <q-card-section>
                          <q-list class="rounded-borders">
                            <q-item>
                              <q-item-section>Popularity</q-item-section>
                              <q-item-section>
                                <q-rating
                                  v-model="
                                    popularityModel[restuaurants[bookedId].id]
                                  "
                                  max="5"
                                  size="1.5em"
                                  color="red"
                                  color-selected="red-9"
                                  icon="favorite_border"
                                  icon-selected="favorite"
                                  icon-half="favorite"
                                  no-dimming
                                  readonly /></q-item-section
                              ><q-item-section avatar
                                ><q-icon
                                  size="sm"
                                  name="info"
                                  color="primary"
                                  @click="scoreDialogFunc('pop')"
                                  style="cursor: pointer"
                                />
                              </q-item-section>
                            </q-item>
                          </q-list>
                          <div
                            v-if="restaurantJsonRel.length"
                            class="card-styling"
                          >
                            <q-list class="rounded-borders">
                              <q-item>
                                <q-item-section
                                  >Fitness for your group</q-item-section
                                >
                                <q-item-section>
                                  <q-rating
                                    v-model="
                                      avrAttractModel[restuaurants[bookedId].id]
                                    "
                                    max="5"
                                    size="1.5em"
                                    color="green"
                                    icon="star_border"
                                    icon-selected="star"
                                    icon-half="star_half"
                                    no-dimming
                                    readonly /></q-item-section
                                ><q-item-section avatar
                                  ><q-icon
                                    size="sm"
                                    name="info"
                                    color="primary"
                                    @click="scoreDialogFunc('avrattr')"
                                    style="cursor: pointer"
                                  />
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <q-list class="rounded-borders">
                              <q-item>
                                <q-item-section
                                  >Similarity to the group which bookmarked this
                                  restaurant</q-item-section
                                >
                                <q-item-section>
                                  <q-rating
                                    v-model="
                                      similarityModel[restuaurants[bookedId].id]
                                    "
                                    size="1.5em"
                                    :max="5"
                                    icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                                    icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                                    readonly /></q-item-section
                                ><q-item-section avatar
                                  ><q-icon
                                    size="sm"
                                    name="info"
                                    color="primary"
                                    @click="
                                      scoreDialogFunc(
                                        'sim',
                                        restuaurants[bookedId].id
                                      )
                                    "
                                    style="cursor: pointer"
                                  />
                                </q-item-section>
                              </q-item>
                            </q-list>
                          </div>
                          <div
                            v-if="
                              extractDissatisfiedsBinary(
                                restuaurants[bookedId].id
                              ) && restaurantJsonRel.length
                            "
                          >
                            <q-separator />
                            <q-list dense>
                              <q-item
                                style="padding-left: 0px; padding-right: 0px"
                                dense
                              >
                                <q-item-section
                                  avatar
                                  dense
                                  style="padding-right: 0px"
                                >
                                  <q-icon
                                    name="warning"
                                    color="yellow"
                                    size="xs"
                                  />
                                </q-item-section>
                                <q-item-section
                                  style="margin-left: -20px; padding-right: 0px"
                                  dense
                                >
                                  {{ sadsList[restuaurants[bookedId].id] }}
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <q-list
                              dense
                              v-if="tripScore[restuaurants[bookedId].id] >= 4"
                            >
                              <q-item
                                style="padding-left: 0px; padding-right: 0px"
                                dense
                              >
                                <q-item-section
                                  avatar
                                  dense
                                  style="padding-right: 0px"
                                >
                                  <q-icon
                                    name="offline_pin"
                                    color="green"
                                    size="xs"
                                    dense
                                  />
                                </q-item-section>
                                <q-item-section
                                  dense
                                  style="margin-left: -20px; padding-right: 0px"
                                >
                                  TripAdvisor score
                                </q-item-section>
                                <q-item-section
                                  dense
                                  style="margin-left: -20px; padding-right: 0px"
                                >
                                  <q-rating
                                    v-model="
                                      tripScore[restuaurants[bookedId].id]
                                    "
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
                              v-if="
                                popularityModel[restuaurants[bookedId].id] >=
                                2.5
                              "
                            >
                              <q-item
                                style="padding-left: 0px; padding-right: 0px"
                                dense
                              >
                                <q-item-section avatar dense>
                                  <q-icon
                                    name="offline_pin"
                                    color="green"
                                    size="xs"
                                  />
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
                                    v-model="
                                      popularityModel[restuaurants[bookedId].id]
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
                                  ></q-rating>
                                </q-item-section>
                              </q-item>
                            </q-list>
                            <q-list dense>
                              <q-item
                                style="padding-left: 0px; padding-right: 0px"
                                dense
                                v-if="
                                  (menuSizeRest[restuaurants[bookedId].id][
                                    'category'
                                  ] /
                                    10) *
                                    5 >
                                  3
                                "
                              >
                                <q-item-section
                                  avatar
                                  dense
                                  style="padding-right: 0px"
                                >
                                  <q-icon
                                    name="offline_pin"
                                    color="green"
                                    size="xs"
                                  />
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
                                    style="
                                      visibility: hidden;
                                      width: 0px;
                                      height: 0px;
                                    "
                                    >{{
                                      (dishrelevancy =
                                        (menuSizeRest[
                                          restuaurants[bookedId].id
                                        ]["category"] /
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
                                  (menuSizeRest[restuaurants[bookedId].id][
                                    'dishes'
                                  ] /
                                    100) *
                                    5 >
                                  3
                                "
                              >
                                <q-item-section
                                  avatar
                                  dense
                                  style="padding-right: 0px"
                                >
                                  <q-icon
                                    name="offline_pin"
                                    color="green"
                                    size="xs"
                                  />
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
                                    style="
                                      visibility: hidden;
                                      width: 0px;
                                      height: 0px;
                                    "
                                    >{{
                                      (dishrelevancy =
                                        (menuSizeRest[
                                          restuaurants[bookedId].id
                                        ]["dishes"] /
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
                              !extractDissatisfiedsBinary(
                                restuaurants[bookedId].id
                              ) && restaurantJsonRel.length
                            "
                          >
                            <!-- <q-separator /> -->
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
                                      v-model="
                                        tripScore[restuaurants[bookedId].id]
                                      "
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
                                          restuaurants[bookedId].id
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
                                          (menuSizeRest[
                                            restuaurants[bookedId].id
                                          ]["category"] /
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
                                          (menuSizeRest[
                                            restuaurants[bookedId].id
                                          ]["dishes"] /
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
                      <q-card-section
                        style="width: 100%; margin-top: 0px; margin-bottom: 0px"
                      >
                        {{ memberDistanceCal(restuaurants[bookedId].id) }}
                        <div v-for="(value, key) in groupInfo" :key="key">
                          {{ value[1] }}'s distance
                          {{ membersDistance[key] }} KM
                        </div>
                        <p></p>
                        <!-- Group's average distance
                  {{ avrDistance(restuaurants[bookedId]) }} KM
                  <p></p> -->
                        <div class="parent">
                          <q-btn
                            color="primary"
                            label="Closer"
                            @click="distance(restuaurants[bookedId])"
                          />
                        </div>
                      </q-card-section>
                    </q-card>
                  </q-card-section>
                </q-card>
              </div>
            </div>
          </div>
        </div>
        <!-- <div v-else class="row no-wrap Flipped" style="overflow-x: auto"> -->
        <div v-else>
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
          <div
            v-for="bookedId in bookmarked"
            :key="bookedId"
            style="width: 100%; margin-bottom: 2px"
          >
            <div style="padding-left: 1px; padding-right: 1px">
              <div v-if="extractDissatisfiedsBinary(restuaurants[bookedId].id)">
                <q-card
                  class="my-card"
                  style="border-color: red; width: 100%; cursor: pointer"
                  flat
                  bordered
                >
                  <div>
                    <img
                      :src="getLogo(restuaurants[bookedId].logo)"
                      style="height: 170px; width: 100%; border-radius: 5px"
                      @click="navigateToRestPage(bookedId)"
                    />
                    <div
                      class="absolute"
                      style="top: 4px; left: 4px; border-radius: 25px"
                    >
                      <div class="q-pa-md" style="padding: 5px">
                        <div class="q-gutter-y-md column">
                          <q-rating
                            v-model="model3"
                            max="1"
                            size="25px"
                            color="red-9"
                            color-selected="red-9"
                            icon="favorite_border"
                            icon-selected="favorite"
                            @click="
                              submitRemoveBookmark(restuaurants[bookedId].id)
                            "
                            style="background: white; border-radius: 3px"
                          />
                        </div>
                      </div>
                      <div
                        class="absolute"
                        style="
                          top: 155px;
                          left: 4px;
                          /* transform: translateX(-90%);
                          transform: translateY(-95%); */
                        "
                      >
                        {{
                          suggestionEvaluation(
                            fariness(bookedId),
                            attractiveness,
                            bookedId
                          )
                        }}
                        <div
                          v-if="suggestionObj[bookedId] >= maxSuggestion"
                          style="margin: 1px; color: green"
                        >
                          <q-btn
                            icon="offline_pin"
                            color="green"
                            size="10px"
                            style="width: 65px; opacity: 0.8"
                            @click="scoreDialogFunc('sug', bookedId)"
                            >Suggested by app</q-btn
                          >
                        </div>
                      </div>
                    </div>
                  </div>

                  <q-card-section style="margin-top: 0px; margin-bottom: 0px">
                    <div class="card-styling">
                      <div v-if="selectedRest === bookedId">
                        <p style="color: green">
                          You have selected this restaurant. You may change your
                          choice by selecting another restaurant.
                        </p>
                      </div>
                      <div class="text-h6 q-mb-xs">
                        {{ restuaurants[bookedId].name }}
                      </div>

                      <!-- <div
                        v-if="sortingType === 'pop'"
                        style="
                          display: inline;
                          width: 100%;
                          margin-bottom: 8px;
                          padding-bottom: 4px;
                        "
                      >
                        Popularity -->
                      <!-- <q-linear-progress
                        :value="popularityObj[restuaurants[bookedId].id]"
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
                              parseInt(
                                parseFloat(
                                  popularityObj[restuaurants[bookedId].id]
                                ).toFixed(2) * 100
                              ) + '%'
                            "
                          />
                        </div>
                      </q-linear-progress> -->
                      <!-- <q-rating
                          v-model="popularityModel[restuaurants[bookedId].id]"
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
                      </div> -->
                      <!-- <div v-if="sortingType === 'avrattr'">
                        Fitness for your group: -->
                      <!-- <q-icon
                        size="xxs"
                        name="info"
                        color="primary"
                        @click="scoreDialogFunc('avrattr')"
                      /> -->
                      <!-- <q-linear-progress
                        :value="avrAttract[restuaurants[bookedId].id]"
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
                              parseFloat(
                                avrAttract[restuaurants[bookedId].id]
                              ).toFixed(2) *
                                100 +
                              '%'
                            "
                          />
                        </div>
                      </q-linear-progress> -->
                      <!-- <q-rating
                          v-model="avrAttractModel[restuaurants[bookedId].id]"
                          size="1.5em"
                          :max="5"
                          color="orange"
                          readonly
                          icon="star_border"
                          icon-selected="star"
                          icon-half="star_half"
                        ></q-rating>
                      </div> -->
                      <!-- <div v-if="sortingType === 'attr'">
                      Attractiveness for
                      {{
                        groupInfo[sortUserId][1] === "Organizer"
                          ? "you"
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
                          attractiveness[sortUserId][restuaurants[bookedId].id]
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
                                    restuaurants[bookedId].id
                                  ]
                                ).toFixed(2) * 100
                              ) + '%'
                            "
                          />
                        </div>
                      </q-linear-progress>
                    </div> -->
                      <!-- <div v-if="sortingType === 'fair'">
                        Group satisfaction equality:&nbsp;&nbsp;&nbsp; -->

                      <!-- <q-linear-progress
                        :value="fariness(restuaurants[bookedId].id)"
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
                                  fariness(restuaurants[bookedId].id)
                                ).toFixed(2) * 100
                              ) + '%'
                            "
                          />
                        </div>
                      </q-linear-progress> -->
                      <!-- <q-rating
                          v-model="fairModel[restuaurants[bookedId].id]"
                          size="1.5em"
                          :max="5"
                          color="orange"
                          icon-selected="img:https://img.icons8.com/ios/100/FD7E14/anime-emoji--v1.png"
                          icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                          readonly
                        ></q-rating>
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
                        :value="fair_attract[restuaurants[bookedId].id]"
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
                                  fair_attract[restuaurants[bookedId].id]
                                ).toFixed(2) * 100
                              ) + '%'
                            "
                          />
                        </div>
                      </q-linear-progress>
                    </div> -->
                      <!-- <div v-if="sortingType === 'sim'"> -->
                      <!-- {{ getSimilarity(JSON.parse(rest).id) }} -->
                      <!-- {{ similarityValue[JSON.parse(restPageInfo).id] }} -->
                      <!-- Similarity to groups who liked this
                        restaurant:&nbsp;&nbsp;&nbsp;
                        <q-icon
                          size="xxs"
                          name="info"
                          color="primary"
                          @click="
                            scoreDialogFunc('sim', restuaurants[bookedId].id)
                          "
                        /><q-rating
                          v-model="similarityModel[restuaurants[bookedId].id]"
                          size="1.5em"
                          :max="5"
                          icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                          icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                          readonly
                        ></q-rating> -->
                      <!-- <q-linear-progress
                        :value="similarityValue[restuaurants[bookedId].id]"
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
                                  restuaurants[bookedId].id
                                ].toFixed(2) * 100
                              ) + '%'
                            "
                          />
                        </div>
                      </q-linear-progress> -->
                      <!-- </div> -->
                      <!-- <q-list
                        class="rounded-borders"
                        style="padding: 0px"
                        v-if="sortingType !== 'pop'"
                      > -->
                      <!-- <q-expansion-item
                        expand-separator
                        icon="favorite_border"
                        label="Popularity"
                        @click="storeGeneralInteraction()"
                      > -->
                      <q-list class="rounded-borders">
                        <q-item>
                          <q-item-section>Popularity</q-item-section>
                          <q-item-section>
                            <q-rating
                              v-model="
                                popularityModel[restuaurants[bookedId].id]
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
                        </q-item>
                      </q-list>
                    </div>
                    <div v-if="restaurantJsonRel.length" class="card-styling">
                      <!-- <q-list class="rounded-borders"> -->
                      <!-- <q-expansion-item
                        expand-separator
                        icon="star_rate"
                        label="Predicted group scores"
                        @click="storeGroupInteraction()"
                      > -->
                      <q-list class="rounded-borders">
                        <q-item>
                          <q-item-section
                            >Fitness for your group</q-item-section
                          >
                          <q-item-section>
                            <q-rating
                              v-model="
                                avrAttractModel[restuaurants[bookedId].id]
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
                        </q-item>
                      </q-list>
                      <q-list class="rounded-borders">
                        <q-item>
                          <q-item-section
                            >Similarity to the group which bookmarked this
                            restaurant</q-item-section
                          >
                          <q-item-section>
                            <q-rating
                              v-model="
                                similarityModel[restuaurants[bookedId].id]
                              "
                              size="1.5em"
                              :max="5"
                              icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                              icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                              readonly
                          /></q-item-section>
                        </q-item>
                      </q-list>
                    </div>
                    <div>
                      <q-separator />
                      <q-list
                        v-if="
                          extractDissatisfiedsBinary(
                            restuaurants[bookedId].id
                          ) && restaurantJsonRel.length
                        "
                        dense
                      >
                        <q-item
                          style="padding-left: 8px; padding-right: 8px"
                          dense
                        >
                          <q-item-section
                            avatar
                            dense
                            style="padding-right: 0px"
                          >
                            <q-icon name="warning" color="yellow" size="xs" />
                          </q-item-section>
                          <q-item-section
                            style="margin-left: -20px; padding-right: 0px"
                            dense
                          >
                            {{ sadsList[restuaurants[bookedId].id] }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                      <q-list v-else>
                        <q-item
                          style="padding-left: 8px; padding-right: 8px"
                          dense
                        >
                          <q-item-section avatar dense>
                            <q-icon
                              name="offline_pin"
                              color="green"
                              size="xs"
                            />
                          </q-item-section>
                          <q-item-section
                            style="margin-left: -20px; padding-right: 0px"
                            >All members will be satisfied with this restaurant.
                          </q-item-section>
                        </q-item>
                      </q-list>
                      <div>
                        <q-list
                          dense
                          v-if="tripScore[restuaurants[bookedId].id] >= 4"
                        >
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
                              <q-icon
                                name="thumb_down_alt"
                                color="red"
                                size="xs"
                              />
                            </q-item-section>
                            <q-item-section
                              dense
                              style="margin-left: -20px; padding-right: 0px"
                            >
                              Restaurant Quality
                            </q-item-section>
                          </q-item>
                        </q-list>
                        <q-list
                          dense
                          v-if="Boolean(restuaurants[bookedId].price_eco)"
                        >
                          <q-item
                            style="padding-left: 8px; padding-right: 8px"
                            dense
                          >
                            <q-item-section avatar dense>
                              <q-icon
                                name="attach_money"
                                color="green"
                                size="xs"
                              />
                            </q-item-section>
                            <q-item-section
                              dense
                              style="margin-left: -20px; padding-right: 0px"
                            >
                              Restaurant prices are economic
                            </q-item-section>
                          </q-item>
                        </q-list>
                        <q-list
                          dense
                          v-if="Boolean(restuaurants[bookedId].price_mid)"
                        >
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
                          v-if="Boolean(restuaurants[bookedId].price_expensive)"
                        >
                          <q-item
                            style="padding-left: 8px; padding-right: 8px"
                            dense
                          >
                            <q-item-section avatar dense>
                              <q-icon
                                name="attach_money"
                                color="red"
                                size="xs"
                              />
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
                              (menuSizeRest[restuaurants[bookedId].id][
                                'category'
                              ] /
                                10) *
                                5 >
                              3.5
                            "
                          >
                            <q-item-section
                              avatar
                              dense
                              style="padding-right: 0px"
                            >
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
                            <q-item-section
                              avatar
                              dense
                              style="padding-right: 0px"
                            >
                              <q-icon
                                name="thumb_down_alt"
                                color="red"
                                size="xs"
                              />
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
                            v-if="
                              popularityModel[restuaurants[bookedId].id] >= 2.5
                            "
                          >
                            <q-item-section
                              avatar
                              dense
                              style="padding-right: 0px"
                            >
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
                              <q-icon
                                name="thumb_down_alt"
                                color="red"
                                size="xs"
                              />
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
                    <!-- <div
                      v-if="
                        !extractDissatisfiedsBinary(
                          restuaurants[bookedId].id
                        ) && restaurantJsonRel.length
                      "
                    >
                      <q-separator />
                      <q-list>
                        <q-item
                          style="padding-left: 8px; padding-right: 8px"
                          dense
                        >
                          <q-item-section avatar dense>
                            <q-icon
                              name="offline_pin"
                              color="green"
                              size="xs"
                            />
                          </q-item-section>
                          <q-item-section
                            style="margin-left: -20px; padding-right: 0px"
                            >All members will be satisfied with this restaurant.
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </div> -->
                  </q-card-section>

                  <!-- <div
                    class="q-pa-md row items-start q-gutter-md"
                    style="padding: 0px; margin: 1px auto"
                  >
                    <p v-if="Boolean(restuaurants[bookedId]['price_eco'])">
                      Price: Economic
                    </p>

                    <p v-if="Boolean(restuaurants[bookedId]['price_mid'])">
                      Price: Mid-range
                    </p>

                    <p
                      v-if="Boolean(restuaurants[bookedId]['price_expensive'])"
                    >
                      Price: Expensive
                    </p>
                    <br />
                    {{ checkValidity() }}
                    <div v-if="String(locationValidity) === 'true'">
                      {{ memberDistanceCal(bookedId) }}
                      <div v-for="(value, key) in groupInfo" :key="key">
                        {{ value[1] }}'s distance {{ membersDistance[key] }} KM
                      </div>
                    </div>
                  </div> -->
                  <div v-if="selectedRest !== bookedId" class="parent">
                    <q-card-section style="margin-top: 0px; margin-bottom: 0px">
                      <q-btn
                        color="primary"
                        label="Select"
                        @click="selectToggleFunc(bookedId)"
                        class="critique-btn"
                        style="padding-top: 0px"
                      />
                    </q-card-section>
                  </div>
                </q-card>
              </div>
              <div v-else>
                <q-card
                  class="my-card"
                  style="border-color: green; width: 100%; cursor: pointer"
                  flat
                  bordered
                >
                  <div>
                    <img
                      :src="getLogo(restuaurants[bookedId].logo)"
                      style="height: 170px; width: 100%; border-radius: 5px"
                      @click="navigateToRestPage(bookedId)"
                    />
                    <div
                      class="absolute"
                      style="top: 4px; left: 4px; border-radius: 25px"
                    >
                      <div class="q-pa-md" style="padding: 5px">
                        <div class="q-gutter-y-md column">
                          <q-rating
                            v-model="model3"
                            max="1"
                            size="25px"
                            color="red-9"
                            color-selected="red-9"
                            icon="favorite_border"
                            icon-selected="favorite"
                            @click="
                              submitRemoveBookmark(restuaurants[bookedId].id)
                            "
                            style="background: white; border-radius: 3px"
                          />
                        </div>
                      </div>
                      <div
                        class="absolute"
                        style="
                          top: 155px;
                          left: 4px;
                          /* transform: translateX(-90%);
                          transform: translateY(-95%); */
                        "
                      >
                        {{
                          suggestionEvaluation(
                            fariness(bookedId),
                            attractiveness,
                            bookedId
                          )
                        }}
                        <div
                          v-if="suggestionObj[bookedId] >= maxSuggestion"
                          style="margin: 1px; color: green"
                        >
                          <q-btn
                            icon="offline_pin"
                            color="green"
                            size="10px"
                            style="width: 65px; opacity: 0.8"
                            @click="scoreDialogFunc('sug', bookedId)"
                            >Suggested by app</q-btn
                          >
                        </div>
                      </div>
                    </div>
                  </div>

                  <q-card-section style="margin-top: 0px; margin-bottom: 0px">
                    <div class="card-styling">
                      <div v-if="selectedRest === bookedId">
                        <p style="color: green">
                          You have selected this restaurant. You may change your
                          choice by selecting another restaurant.
                        </p>
                      </div>
                      <div class="text-h6 q-mb-xs">
                        {{ restuaurants[bookedId].name }}
                      </div>

                      <q-list class="rounded-borders">
                        <q-item>
                          <q-item-section>Popularity</q-item-section>
                          <q-item-section>
                            <q-rating
                              v-model="
                                popularityModel[restuaurants[bookedId].id]
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
                        </q-item>
                      </q-list>
                    </div>
                    <div v-if="restaurantJsonRel.length" class="card-styling">
                      <!-- <q-list class="rounded-borders"> -->
                      <!-- <q-expansion-item
                        expand-separator
                        icon="star_rate"
                        label="Predicted group scores"
                        @click="storeGroupInteraction()"
                      > -->
                      <q-list class="rounded-borders">
                        <q-item>
                          <q-item-section
                            >Fitness for your group</q-item-section
                          >
                          <q-item-section>
                            <q-rating
                              v-model="
                                avrAttractModel[restuaurants[bookedId].id]
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
                        </q-item>
                      </q-list>
                      <q-list class="rounded-borders">
                        <q-item>
                          <q-item-section
                            >Similarity to the group which bookmarked this
                            restaurant</q-item-section
                          >
                          <q-item-section>
                            <q-rating
                              v-model="
                                similarityModel[restuaurants[bookedId].id]
                              "
                              size="1.5em"
                              :max="5"
                              icon="img:https://img.icons8.com/ios/50/FD7E14/conference-call--v1.png"
                              icon-selected="img:https://img.icons8.com/ios-filled/50/FD7E14/conference-call.png"
                              readonly
                          /></q-item-section>
                        </q-item>
                      </q-list>
                    </div>
                    <div
                      v-if="
                        extractDissatisfiedsBinary(restuaurants[bookedId].id) &&
                        restaurantJsonRel.length
                      "
                    >
                      <q-separator />
                      <q-list dense>
                        <q-item
                          style="padding-left: 0px; padding-right: 0px"
                          dense
                        >
                          <q-item-section
                            avatar
                            dense
                            style="padding-right: 0px"
                          >
                            <q-icon name="warning" color="yellow" size="xs" />
                          </q-item-section>
                          <q-item-section
                            style="margin-left: -20px; padding-right: 0px"
                            dense
                          >
                            {{ sadsList[restuaurants[bookedId].id] }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                      <q-list
                        dense
                        v-if="tripScore[restuaurants[bookedId].id] >= 4"
                      >
                        <q-item
                          style="padding-left: 0px; padding-right: 0px"
                          dense
                        >
                          <q-item-section
                            avatar
                            dense
                            style="padding-right: 0px"
                          >
                            <q-icon
                              name="offline_pin"
                              color="green"
                              size="xs"
                              dense
                            />
                          </q-item-section>
                          <q-item-section
                            dense
                            style="margin-left: -20px; padding-right: 0px"
                          >
                            TripAdvisor score
                          </q-item-section>
                          <q-item-section
                            dense
                            style="margin-left: -20px; padding-right: 0px"
                          >
                            <q-rating
                              v-model="tripScore[restuaurants[bookedId].id]"
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
                        v-if="popularityModel[restuaurants[bookedId].id] >= 2.5"
                      >
                        <q-item
                          style="padding-left: 0px; padding-right: 0px"
                          dense
                        >
                          <q-item-section avatar dense>
                            <q-icon
                              name="offline_pin"
                              color="green"
                              size="xs"
                            />
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
                              v-model="
                                popularityModel[restuaurants[bookedId].id]
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
                            ></q-rating>
                          </q-item-section>
                        </q-item>
                      </q-list>
                      <q-list dense>
                        <q-item
                          style="padding-left: 0px; padding-right: 0px"
                          dense
                          v-if="
                            (menuSizeRest[restuaurants[bookedId].id][
                              'category'
                            ] /
                              10) *
                              5 >
                            3
                          "
                        >
                          <q-item-section
                            avatar
                            dense
                            style="padding-right: 0px"
                          >
                            <q-icon
                              name="offline_pin"
                              color="green"
                              size="xs"
                            />
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
                              style="
                                visibility: hidden;
                                width: 0px;
                                height: 0px;
                              "
                              >{{
                                (dishrelevancy =
                                  (menuSizeRest[restuaurants[bookedId].id][
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
                            ></q-rating>
                          </q-item-section>
                        </q-item>
                      </q-list>
                      <q-list dense>
                        <q-item
                          style="padding-left: 0px; padding-right: 0px"
                          dense
                          v-if="
                            (menuSizeRest[restuaurants[bookedId].id]['dishes'] /
                              100) *
                              5 >
                            3
                          "
                        >
                          <q-item-section
                            avatar
                            dense
                            style="padding-right: 0px"
                          >
                            <q-icon
                              name="offline_pin"
                              color="green"
                              size="xs"
                            />
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
                              style="
                                visibility: hidden;
                                width: 0px;
                                height: 0px;
                              "
                              >{{
                                (dishrelevancy =
                                  (menuSizeRest[restuaurants[bookedId].id][
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
                            ></q-rating>
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </div>
                    <div
                      v-if="
                        !extractDissatisfiedsBinary(
                          restuaurants[bookedId].id
                        ) && restaurantJsonRel.length
                      "
                    >
                      <q-separator />
                      <!-- At least one of you will not be satisfied with this
                    restaurant. -->
                      <q-list
                        v-if="
                          extractDissatisfiedsBinary(
                            restuaurants[bookedId].id
                          ) && restaurantJsonRel.length
                        "
                        dense
                      >
                        <q-item
                          style="padding-left: 8px; padding-right: 8px"
                          dense
                        >
                          <q-item-section
                            avatar
                            dense
                            style="padding-right: 0px"
                          >
                            <q-icon name="warning" color="yellow" size="xs" />
                          </q-item-section>
                          <q-item-section
                            style="margin-left: -20px; padding-right: 0px"
                            dense
                          >
                            {{ sadsList[restuaurants[bookedId].id] }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                      <q-list v-else>
                        <q-item
                          style="padding-left: 8px; padding-right: 8px"
                          dense
                        >
                          <q-item-section avatar dense>
                            <q-icon
                              name="offline_pin"
                              color="green"
                              size="xs"
                            />
                          </q-item-section>
                          <q-item-section
                            style="margin-left: -20px; padding-right: 0px"
                            >All members will be satisfied with this restaurant.
                          </q-item-section>
                        </q-item>
                      </q-list>
                      <div>
                        <q-list
                          dense
                          v-if="tripScore[restuaurants[bookedId].id] >= 4"
                        >
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
                              <q-icon
                                name="thumb_down_alt"
                                color="red"
                                size="xs"
                              />
                            </q-item-section>
                            <q-item-section
                              dense
                              style="margin-left: -20px; padding-right: 0px"
                            >
                              Restaurant Quality
                            </q-item-section>
                          </q-item>
                        </q-list>
                        <q-list
                          dense
                          v-if="Boolean(restuaurants[bookedId].price_eco)"
                        >
                          <q-item
                            style="padding-left: 8px; padding-right: 8px"
                            dense
                          >
                            <q-item-section avatar dense>
                              <q-icon
                                name="attach_money"
                                color="green"
                                size="xs"
                              />
                            </q-item-section>
                            <q-item-section
                              dense
                              style="margin-left: -20px; padding-right: 0px"
                            >
                              Restaurant prices are economic
                            </q-item-section>
                          </q-item>
                        </q-list>
                        <q-list
                          dense
                          v-if="Boolean(restuaurants[bookedId].price_mid)"
                        >
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
                          v-if="Boolean(restuaurants[bookedId].price_expensive)"
                        >
                          <q-item
                            style="padding-left: 8px; padding-right: 8px"
                            dense
                          >
                            <q-item-section avatar dense>
                              <q-icon
                                name="attach_money"
                                color="red"
                                size="xs"
                              />
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
                              (menuSizeRest[restuaurants[bookedId].id][
                                'category'
                              ] /
                                10) *
                                5 >
                              3.5
                            "
                          >
                            <q-item-section
                              avatar
                              dense
                              style="padding-right: 0px"
                            >
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
                            <q-item-section
                              avatar
                              dense
                              style="padding-right: 0px"
                            >
                              <q-icon
                                name="thumb_down_alt"
                                color="red"
                                size="xs"
                              />
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
                            v-if="
                              popularityModel[restuaurants[bookedId].id] >= 2.5
                            "
                          >
                            <q-item-section
                              avatar
                              dense
                              style="padding-right: 0px"
                            >
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
                              <q-icon
                                name="thumb_down_alt"
                                color="red"
                                size="xs"
                              />
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

                  <!-- <div
                    class="q-pa-md row items-start q-gutter-md"
                    style="padding: 0px; margin: 1px auto"
                  >
                    <p v-if="Boolean(restuaurants[bookedId]['price_eco'])">
                      Price: Economic
                    </p>

                    <p v-if="Boolean(restuaurants[bookedId]['price_mid'])">
                      Price: Mid-range
                    </p>

                    <p
                      v-if="Boolean(restuaurants[bookedId]['price_expensive'])"
                    >
                      Price: Expensive
                    </p>
                    <br />
                    {{ checkValidity() }}
                    <div v-if="String(locationValidity) === 'true'">
                      {{ memberDistanceCal(bookedId) }}
                      <div v-for="(value, key) in groupInfo" :key="key">
                        {{ value[1] }}'s distance {{ membersDistance[key] }} KM
                      </div>
                    </div>
                  </div> -->
                  <div v-if="selectedRest !== bookedId" class="parent">
                    <q-card-section style="margin-top: 0px; margin-bottom: 0px">
                      <q-btn
                        color="primary"
                        label="Select"
                        @click="selectToggleFunc(bookedId)"
                        class="critique-btn"
                        style="padding-top: 8px"
                      />
                    </q-card-section>
                  </div>
                </q-card>
              </div>
            </div>
          </div>
        </div>
        <!-- <q-dialog v-model="scoreDialog">
          <q-card>
            <q-card-section>
              <div class="text-h6">Alert</div>
            </q-card-section>
            <q-card-section class="q-pt-none" align="justify">
              {{ scoreExplanation }}
            </q-card-section>
            <q-card-actions align="right">
              <q-btn flat label="OK" color="primary" v-close-popup />
            </q-card-actions>
          </q-card>
        </q-dialog> -->
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
                  <q-item-label>Remove filter</q-item-label>
                </q-item-section>
              </q-item>
              <q-separator />
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
              <q-separator />
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
              <q-separator />
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
    <!-- <div v-else style="height: 100vh">
      {{ similarityValidity }}
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
    </div> -->
  </div>
  <div v-if="bookmarkedLength === 0" style="height: 100vh">
    <div class="no-tasks absolute-center text-h5 text-primary text-center">
      Either you have not bookmarked any restaurant, or you need to wait to
      upload the bookmarked restaurants.
    </div>
  </div>
  <!-- </div> -->
</template>

<script>
import axios from "axios";
import { ref } from "vue";
export default {
  props: [
    "groupInfo",
    "groupId",
    "organizerId",
    "userPreferenceList",
    "critiqueRange",
  ],
  emits: ["critiqueIssued", "RestSelected", "goToGroupPage", "activeRevision"],

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
      menuSizeRest: {},
      menuSizeValidity: false,
      sadsList: {},
      similarityValidity: false,
      similarityExplanation: "",
      positionExplan: ref("bottom"),
      userAttractive: {},
      restaurantJsonPop: {},
      icons: [
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
        "sentiment_very_satisfied",
      ],
      selectedRest: -1,
      menuSizeGlobal: {},
      attractivenessModel: {},
      fairModel: {},
      similarityModel: {},
      avrAttractModel: {},
      popularityModelLoad: false,
      popularityModel: {},
      bookmarkedLength: 0,
      bookedLengthValidation: false,
      pageLoadedAll: false,
      sortUserId: -1,
      sortingType: "",
      pageLoadedSimilarity: false,
      pageRestLoead: false,
      avrAttract: {},
      selectedPopularityObj: {},
      selectionLoad: false,
      popularityObj: {},
      endOfSession: false,
      selectToggle: false,
      maxSuggestion: 0,
      links: require(`../assets/external_link.json`),
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
      val1: ref(false),
      val2: ref(false),
      val3: ref(false),
      val4: ref(false),
      val5: ref(false),
      val6: ref(false),
      val7: ref(false),
      val8: ref(false),
      val9: ref(false),
      val10: ref(false),
      val11: ref(false),
      val12: ref(false),
      val13: ref(false),
      val14: ref(false),
      shape: ref("line"),
      textareaModel: "",
      fair_attract: {},
      pageLoaded: false,
      priceDialog: ref(false),
      positionPrice: ref("bottom"),
      scoreDialog: ref(false),
      scoreExplanation: "",
      bannerToggle: true,
      explainRestId: 0,
      simRestExp: {},
    };
  },
  methods: {
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
    getIndiExplan(menu, indiId, gInfo, name) {
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
      explanation = explanation.charAt(0).toUpperCase() + explanation.slice(1);
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
          this.similarityExplanation = explanation;
          this.scoreDialog = ref(true);
        }
      });
    },
    menuSizeCounter(restId, counter, counterStop) {
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
          if (counter < counterStop) {
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
    bannerToggler() {
      this.bannerToggle = false;
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
    bannerValidation(restaurantObject) {
      this.bannerToggle = true;
      const threshold = 0.6;
      const groupSize = Object.keys(this.groupInfo).length;
      for (var restaurant of restaurantObject) {
        const userList = Object.keys(this.groupInfo);
        var membersSatsfaction = false;
        var happyMembersCount = 0;
        if (typeof this.attractiveness === "undefined") {
          this.bannerToggle = false;
        } else {
          for (const userKey of userList) {
            if (typeof this.attractiveness[userKey] === "undefined") {
              happyMembersCount++;
            } else if (this.attractiveness[userKey][restaurant] > threshold) {
              happyMembersCount++;
            }
          }
          if (happyMembersCount === groupSize) {
            this.bannerToggle = false;
          }
        }
      }
    },
    setTimeoutReset() {
      setTimeout(function () {
        location.reload();
      }, 4000);
    },
    scoreDialogFunc(dialogType, restIdGet) {
      if (dialogType === "pop") {
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
        this.scoreDialog = ref(true);
        this.scoreExplanation = "avrattr";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting Average attractiveness Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (dialogType === "fair") {
        this.scoreDialog = ref(true);
        this.extractDissatisfieds(restIdGet);
        this.scoreExplanation = "fair";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting Fairness Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (dialogType === "attrfair") {
        this.scoreDialog = ref(true);
        this.scoreExplanation = "attrfair";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction:
            "Visiting Fairness and Average Attractiveness Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (dialogType === "sim") {
        this.similarityExplanationFunc(restIdGet);
        this.scoreExplanation = "sim";
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting Similarity Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (dialogType === "sug") {
        this.scoreExplanation = "sug";
        this.scoreDialog = ref(true);
        var interactionData = {
          group_id: this.group_id_intract,
          interaction: "Visiting App Suggestion Explanation",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
      } else if (dialogType === "trip") {
        this.scoreExplanation = "trip";
        this.scoreDialog = ref(true);
      } else if (dialogType === "dishDiv") {
        this.scoreExplanation = "dishDiv";
        this.scoreDialog = ref(true);
      } else if (dialogType === "categ") {
        this.scoreExplanation = "categ";
        this.scoreDialog = ref(true);
      }
    },
    openPriceCritique() {
      this.positionPrice = ref("bottom");
      this.priceDialog = ref(true);
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
      var flag11 = true;
      var flag12 = true;
      var flag13 = true;
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
        (this.val1 === false) &
        (this.val2 === false) &
        (this.val3 === false) &
        (this.val4 === false) &
        (this.val10 === false) &
        (this.val11 === false) &
        (this.val14 === false)
      ) {
        flag11 = false;
        this.$q.notify({
          message: "Please answer the question 11.",
          icon: "announcement",
          color: "red",
        });
      }
      if (
        (this.val5 === false) &
        (this.val6 === false) &
        (this.val7 === false) &
        (this.val8 === false) &
        (this.val9 === false) &
        (this.val12 === false) &
        (this.val13 === false)
      ) {
        // flag12 = false;
        // this.$q.notify({
        //   message: "Please answer the question 12.",
        //   icon: "announcement",
        //   color: "red",
        // });
      }
      if (this.shape === "line") {
        // flag13 = false;
        // this.$q.notify({
        //   message: "Please answer the question 13.",
        //   icon: "announcement",
        //   color: "red",
        // });
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
        (flag10 === true) &
        (flag11 === true) &
        (flag12 === true) &
        (flag13 === true)
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
          f1: this.val1,
          f2: this.val2,
          f3: this.val3,
          f4: this.val4,
          f5: this.val10,
          f6: this.val11,
          f7: this.val14,
          f8: this.val5,
          f8: this.val6,
          f10: this.val7,
          f11: this.val8,
          f12: this.val9,
          f13: this.val12,
          f14: this.val13,
          f15: this.shape,
          c1: this.textareaModel,
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
        sessionStorage.setItem(
          "popularityObj",
          JSON.stringify(this.popularityObj)
        );
      });
    },
    selectedPopularity(restId) {
      var url =
        "http://46.18.25.97:8050/restaurant/select/popularity/" +
        String(restId);
      axios.get(url).then((response) => {
        this.selectedPopularityObj[restId] = 0;
        this.selectedPopularityObj[restId] = parseFloat(
          JSON.parse(response.data)
        );
        this.selectionLoad = true;
        sessionStorage.setItem(
          "selectedPopularity",
          JSON.stringify(this.selectedPopularityObj)
        );
      });
    },
    selectToggleFunc(bookedId) {
      this.bookedRestId = bookedId;
      this.selectToggle = !this.selectToggle;
    },
    select(bookedId, fair, attr, sim) {
      this.selectToggle = !this.selectToggle;
      this.selectedRest = bookedId;
      this.bookedRestId = bookedId;
      this.navigated = [bookedId];
      this.restPageActive = true;
      if (this.organizerId !== -1) {
        var selectedDataOrganizer = {
          user_id: parseInt(Object.keys(this.organizerId)[0]),
          organizer: 0,
          member: 0,
          restaurant_id: parseInt(bookedId),
        };
        axios
          .post(
            "http://46.18.25.97:8050/organizer/selected",
            selectedDataOrganizer
          )
          .then(this.$emit("RestSelected"));
        // .then(this.$emit("RestSelected"));
      }
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
        // this.endOfSession = true;
      });
    },
    suggestionEvaluation(fair, attract, idRest) {
      var attractSum = 0;
      const urlmnue = "http://46.18.25.97:8050/restaurant/menu/" + idRest;
      axios.get(urlmnue).then((response) => {
        var menuSize = 0;
        var menuList = JSON.parse(JSON.stringify(response.data));
        for (var dishes of Object.values(menuList)) {
          menuSize = menuSize + dishes.length;
        }
        for (var restAttract of Object.values(attract)) {
          attractSum = attractSum + restAttract[idRest];
        }
        var attrAvr = attractSum / Object.keys(attract).length;
        if (attrAvr * fair + menuSize / 10000 > this.maxSuggestion) {
          this.maxSuggestion = attrAvr * fair + menuSize / 10000;
        }
        this.suggestionObj[idRest] = attrAvr * fair + menuSize / 10000;
      });
    },
    getLogo(logo) {
      return require(`../assets/logo/` + String(logo));
    },
    getLogoIn(logo) {
      return require(`../assets/logo/logo/` + String(logo));
    },
    backToBookmark() {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Back to bookmark page",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.restPageActive = false;
    },
    // getSimilarity(restaurantId, bookedLength) {
    //   if (this.restaurantJsonRel.length) {
    //     const dataSimilarity = {
    //       restaurantId: restaurantId,
    //       groupId: this.groupId,
    //     };
    //     const url = "http://46.18.25.97:8050/similarity";
    //     axios.post(url, dataSimilarity).then((response) => {
    //       this.similarityValue[restaurantId] = response.data;
    //       this.similarityObj[restaurantId] = response.data;
    //       this.similarityModelFunc(restaurantId, response.data);
    //       if (bookedLength === Object.keys(this.similarityValue).length) {
    //         this.pageLoadedSimilarity = true;
    //       }
    //       return response.data;
    //     });
    //   } else {
    //     this.similarityModelFunc(restaurantId, 0);
    //     this.similarityValue[restaurantId] = 0;
    //     if (bookedLength === Object.keys(this.similarityValue).length) {
    //       this.pageLoadedSimilarity = true;
    //     }
    //     return 0;
    //   }
    // },
    getSimilarity(restaurantId, bookedLength) {
      this.similarityValidity = false;
      if (this.restaurantJsonRel.length === 0) {
        this.similarityValidity = true;
      }
      if (this.restaurantJsonRel.length) {
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
                  if (this.bookmarkedLength === bookedLength) {
                    this.similarityValidity = true;
                  }
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
                    sutiability++;
                  }
                }
                sutiability = sutiability / Object.keys(similarityObj).length;
                this.similarityValue[restaurantId] = sutiability;
                this.similarityModelFunc(restaurantId, sutiability);
                if (this.bookmarkedLength === bookedLength) {
                  this.similarityValidity = true;
                }
              }
            });
          } else {
            this.similarityValue[restaurantId] = 0;
            this.similarityModelFunc(restaurantId, 0);
            if (
              bookedLength === this.restaurantJsonRel.length ||
              this.restaurantJsonRel.length === 0
            ) {
              this.similarityValidity = true;
            }
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
      //     // return 1;
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
      //

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
    fairness_attractiveness() {
      var fair_attract_max = 0.000001;
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
    popPercentage(getRestId) {
      if (this.popularityObj[getRestId] === 1) {
        return "This restaurant is the most popular restaurant in this application.";
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
        return portion;
      }
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
    scrollToTop() {
      window.scrollTo(0, 0);
    },
    price(range) {
      this.priceDialog = ref(false);
      if (range === "rem") {
        var rangeSend = "";
      } else {
        var rangeSend = range;
      }
      sessionStorage.setItem("relevanceValidation", false);
      sessionStorage.setItem("attractivenessValidation", false);
      sessionStorage.setItem("SimilarityValidation", false);
      this.$emit("critiqueIssued", rangeSend);
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Pice " + String(range) + "added",
      };
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
    },
    submitRemoveBookmark(restaurantId) {
      if (this.restPageActive === true) {
        this.restPageActive = false;
        this.navigated = [];
      }
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
      this.model3 = ref(1);
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
    avergeAttr(rest) {
      for (var rest of Object.keys(this.restaurantJsonRel)) {
        var sum = 0;
        var count = 0;
        for (var userId of Object.keys(this.groupInfo)) {
          if (typeof this.attractiveness[userId] !== "undefined") {
            count++;
            sum =
              sum +
              this.attractiveness[userId][
                JSON.parse(this.restaurantJsonRel[rest]).id
              ];
          }
        }
        if (count > 0) {
          this.avrAttract[JSON.parse(this.restaurantJsonRel[rest]).id] =
            sum / count;
          this.averAttrModleFunc(
            JSON.parse(this.restaurantJsonRel[rest]).id,
            sum / count
          );
          this.fairnessModelFunc(JSON.parse(this.restaurantJsonRel[rest]).id);
        } else {
          this.avrAttract[JSON.parse(this.restaurantJsonRel[rest]).id] = sum;
          this.averAttrModleFunc(
            JSON.parse(this.restaurantJsonRel[rest]).id,
            sum
          );
          this.fairnessModelFunc(JSON.parse(this.restaurantJsonRel[rest]).id);
        }
      }
    },
    populairtyModelFunc() {
      var popularityObjTemp = {};
      var counter = 0;
      if (JSON.parse(sessionStorage.getItem("popularityValidation")) !== true) {
        for (var resturant of Object.values(this.restaurantJsonPop)) {
          var restIdGet = JSON.parse(resturant).id;
          var url =
            "http://46.18.25.97:8050/restaurant/popularity/dict/" +
            String(restIdGet);
          axios.get(url).then((response) => {
            popularityObjTemp[parseInt(Object.keys(response.data)[0])] =
              parseFloat(Object.values(response.data)[0]);
            counter++;
            if (counter === this.restaurantJsonPop.length) {
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
    attractivenessModelFunc() {
      this.attractivenessModel = {};
      for (var userId of Object.keys(this.attractiveness)) {
        var userObject = {};
        for (var [key, value] of Object.entries(this.attractiveness[userId])) {
          if (value <= 0) {
            userObject[key] = ref(0);
          } else if (value <= 0.12) {
            userObject[key] = ref(0.5);
          } else if (value <= 0.22) {
            userObject[key] = ref(1);
          } else if (value <= 0.32) {
            userObject[key] = ref(1.5);
          } else if (value <= 0.42) {
            userObject[key] = ref(2);
          } else if (value <= 0.52) {
            userObject[key] = ref(2.5);
          } else if (value <= 0.62) {
            userObject[key] = ref(3);
          } else if (value <= 0.72) {
            userObject[key] = ref(3.5);
          } else if (value <= 0.82) {
            userObject[key] = ref(4);
          } else if (value <= 0.92) {
            userObject[key] = ref(4.5);
          } else {
            userObject[key] = ref(5);
          }
        }
        this.attractivenessModel[userId] = userObject;
      }
    },
  },
  mounted() {
    const url = "http://46.18.25.97:8050/recommendations/get/popularity/count";
    axios.get(url).then((response) => {
      this.countPopularity = response.data;
      var srotValue = parseInt(JSON.parse(sessionStorage.getItem("sorting")));
      if (srotValue === -1) {
        this.sortingType = "pop";
      } else if (srotValue === 0) {
        this.sortingType = "attr";
        this.sortUserId = sessionStorage.getItem("user_id");
      } else if (srotValue === 1) {
        this.sortingType = "fair";
      } else if (srotValue === 2) {
        this.sortingType = "attrfair";
      } else if (srotValue === 4) {
        this.sortingType = "avrattr";
      } else if (srotValue === 5) {
        this.sortingType = "sim";
      }
      var bookedLength = 0;
      this.bookedLengthValidation = false;
      url = "http://46.18.25.97:8050/bookmarked/" + String(this.groupId);
      axios.get(url).then((response) => {
        this.bookmarkedLength = Object.keys(
          JSON.parse(JSON.stringify(response.data))
        ).length;
        if (String(sessionStorage.getItem("menuSizeValidity")) !== "true") {
          var counting = 0;
          for (var resId in Object.keys(
            JSON.parse(JSON.stringify(response.data))
          )) {
            this.menuSizeCounter(resId, counting, this.bookmarkedLength);
          }
        } else {
          this.menuSizeRest = JSON.parse(sessionStorage.getItem("MenuSize"));
          this.menuSizeValidity = true;
        }
        this.bookedLengthValidation = true;
      });
      var url =
        "http://46.18.25.97:8050/recommendations/popularity/" + this.groupId;
      // if (JSON.parse(sessionStorage.getItem("relevanceValidation")) !== true) {
      axios.get(url).then((response) => {
        this.restaurantJsonPop = JSON.parse(JSON.stringify(response.data));
        this.populairtyModelFunc();
      });
      // if (String(sessionStorage.getItem("Selected")) === "true") {
      //   this.endOfSession = true;
      // } else {
      //   this.endOfSession = false;
      // }
      var url =
        "http://46.18.25.97:8050/recommendations/relevance/withoutfiltering/" +
        this.groupId;
      // if (JSON.parse(sessionStorage.getItem("relevanceValidation")) !== true) {
      axios.get(url).then((response) => {
        this.restaurantJsonRel = JSON.parse(JSON.stringify(response.data));
        if (this.restaurantJsonRel.length === 0) {
          this.similarityValidity = true;
        }
        url = "http://46.18.25.97:8050/bookmarked/" + String(this.groupId);
        axios.get(url).then((response) => {
          bookedLength = JSON.parse(JSON.stringify(response.data)).length;
          var counterSim = 0;
          for (var bookedrest of response.data) {
            counterSim++;
            this.getSimilarity(bookedrest, counterSim);
            this.bookmarked.push(bookedrest);

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

              this.selectionLoad = true;
            }
            var urlRest =
              "http://46.18.25.97:8050/restaurant/" + String(bookedrest);
            axios.get(urlRest).then((response) => {
              this.restuaurants[response.data.id] = response.data;
              const urlAttract =
                "http://46.18.25.97:8050/recommendations/attractiveness/" +
                this.groupId;

              axios.get(urlAttract).then((response) => {
                this.attractiveness = JSON.parse(JSON.stringify(response.data));
                if (this.restaurantJsonRel.length > 0) {
                  this.fairness_attractiveness();
                  this.avergeAttr();
                  this.attractivenessModelFunc();
                  this.bannerValidation(this.bookmarked);
                } else {
                  this.bannerValidation(this.bookmarked);
                }

                this.pageLoaded = true;
              });
              if (Object.keys(this.restuaurants).length === bookedLength) {
                this.pageLoadedAll = true;
              }
            });
            this.pageLoadedSimilarity = true;
            if (this.restaurantJsonRel === 0) {
              this.similarityValidity = true;
            }
          }
        });
      });
      // } else {
      //   var url =
      //     "http://46.18.25.97:8050/recommendations/relevance/withoutfiltering/" +
      //     this.groupId;
      //   axios.get(url).then((response) => {
      //     this.restaurantJsonRel = JSON.parse(JSON.stringify(response.data));
      //     url = "http://46.18.25.97:8050/bookmarked/" + String(this.groupId);
      //     axios.get(url).then((response) => {
      //       this.pageLoadedAll = true;
      //       bookedLength = JSON.parse(JSON.stringify(response.data)).length;
      //       const urlAttract =
      //         "http://46.18.25.97:8050/recommendations/attractiveness/" +
      //         this.groupId;
      //       if (
      //         JSON.parse(sessionStorage.getItem("attractivenessValidation")) !==
      //         true
      //       ) {
      //         axios.get(urlAttract).then((response) => {
      //           this.attractiveness = JSON.parse(JSON.stringify(response.data));
      //           if (this.restaurantJsonRel.length > 0) {
      //             this.fairness_attractiveness();
      //             this.avergeAttr();
      //           }
      //         });
      //       } else {
      //         this.attractiveness = JSON.parse(
      //           sessionStorage.getItem("attractiveness")
      //         );
      //         if (this.restaurantJsonRel.length > 0) {
      //           this.fairness_attractiveness();
      //           this.avergeAttr();
      //         }
      //       }

      //       for (var bookedrest of response.data) {
      //         if (
      //           JSON.parse(sessionStorage.getItem("SimilarityValidation")) ===
      //           true
      //         ) {
      //           this.similarityValue = JSON.parse(
      //             sessionStorage.getItem("SimilarityValue")
      //           );
      //           this.pageLoadedSimilarity = true;
      //         } else {
      //           this.getSimilarity(bookedrest, bookedLength);
      //         }
      //         this.bookmarked.push(bookedrest);
      //         if (
      //           JSON.parse(sessionStorage.getItem("popularityValidation")) !==
      //           true
      //         ) {
      //           this.popularity(JSON.parse(resturant).id);
      //         } else {
      //           this.popularityObj = JSON.parse(
      //             sessionStorage.getItem("popularityObj")
      //           );
      //         }
      //         if (
      //           JSON.parse(
      //             sessionStorage.getItem("selectedPopularityValidation")
      //           ) !== true
      //         ) {
      //           this.selectedPopularity(JSON.parse(resturant).id);
      //         } else {
      //           this.selectedPopularityObj = JSON.parse(
      //             sessionStorage.getItem("selectedPopularity")
      //           );
      //           this.selectionLoad = true;
      //         }
      //         var urlRest =
      //           "http://46.18.25.97:8050/restaurant/" + String(bookedrest);
      //         axios.get(urlRest).then((response) => {
      //           this.restuaurants[response.data.id] = response.data;
      //           if (Object.keys(this.restuaurants).length === bookedLength) {
      //             this.pageLoaded = true;
      //           }
      //         });
      //       }
      //     });
      //   });
      // }
    });
  },
};
</script>

<style scoped>
.my-card {
  width: 100%;
}
.question {
  padding: 3px auto;
  margin: 5px auto;
}
.button-back {
  margin-top: 5px;
  margin-left: 5px;
  position: fixed;
  z-index: 30;
}
.Flipped,
.Flipped .Content {
  transform: rotateX(180deg);
  -ms-transform: rotateX(180deg); /* IE 9 */
  -webkit-transform: rotateX(180deg); /* Safari and Chrome */
}
.sadnessActive {
  border-color: red;
}
.sadnessNotActive {
  border-color: green;
}
.card-styling {
  padding-top: 0px;
  padding-bottom: 0px;
}
.memberExplan {
  padding-left: 0px;
  padding-right: 0px;
}
.q-chip {
  cursor: pointer;
}
</style>
