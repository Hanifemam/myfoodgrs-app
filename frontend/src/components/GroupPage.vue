<template class>
  <div style="overflow: hidden">
    <!-- <q-banner
      v-if="disclimer"
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
        Please be aware that each of your accounts is associated with a distinct
        group comprising different members. Consequently, when making decision
        about suitable restaurant, please consider the group members associated
        to the CURRENT GROUP. Please DO NOT forget to
        <strong>SELECT</strong> one of the bookmarked restaurants in the
        bookmark page to finish the second stage of the experiment. If you have
        already done the second stage you do not need to repeat it.
      </p>
      <template v-slot:action>
        <q-btn
          size="sm"
          flat
          color="white"
          label="OK"
          @click="disclimer = !disclimer"
        />
      </template>
    </q-banner> -->
    <!-- {{ scrollToTop() }} -->
    <q-dialog v-model="infoDialog">
      <!-- <div class="q-pa-md" style="width: 100%"> -->
      <q-card class="my-card" style="width: 100%">
        <q-btn icon="close" flat round dense v-close-popup />
        <q-form
          @submit="onSubmitInfo"
          @reset="onResetInfo"
          class="q-gutter-md"
          style="
            padding-left: 16px;
            padding-right: 16px;
            padding-top: 16px;
            padding-bottom: 16px;
          "
        >
          <div class="q-pa-md" style="margin-top: 0px">
            <div class="q-gutter-md">
              <p style="text-align: justify">
                Please add some of the following information about
                <strong>{{ memberInfoName }}</strong
                >. If you do not have any information get popular food
                preferences by clicking on SUBMIT without inserting any
                information.
              </p>
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

          <q-input
            filled
            type="number"
            v-model="memberAgeInfo"
            label="Age"
            lazy-rules
            :rules="[
              (val) => (val !== null && val !== '') || 'Please type your age',
              (val) => (val >= 0 && val < 100) || 'Please type a real age',
            ]"
            style="width: 93%"
          />
          <!-- <div
            class="q-pa-md row items-start q-gutter-md"
            style="padding: 2px 2px 2px 0px; margin: 0px 0px 0px 0px"
          >
            <p style="margin-top: 0px; margin-bottom: 0px">
              Add the preferences that you think {{ memberInfoName }} may
              like:
            </p>
            <div
              v-for="(food, indexInner) in foodsCategory"
              :key="indexInner"
              style="padding: 2px 2px 2px 0px; margin-top: 0px 0px 0px 0px"
            >
              <q-card
                :class="
                  isInArray(food, memberPreference[name])
                    ? categoryCardColor[index + 1]
                    : categoryCardColor[0]
                "
                @click="addPreferences(name, food, memberInfoName)"
                style="cursor: pointer"
              >
                <q-card-section style="padding: 6px 6px 6px 6px">
                  {{ food_name_change(food) }}
                </q-card-section>
              </q-card>
            </div>
          </div> -->
          <div
            class="q-pa-md row items-start q-gutter-md"
            style="padding: 2px 2px 2px 0px; margin: 0px 0px 0px 6px"
          >
            <p style="margin-top: 0px; margin-bottom: 0px">
              Which one of the following cuisines you think that
              {{ memberInfoName }} may like:
            </p>
            <div
              class="q-pa-md"
              style="padding: 2px 2px 2px 0px; margin: 0px 0px 0px 3px"
            >
              <div
                class="q-gutter-sm"
                style="margin-left: 0px; margin-top: 0px"
              >
                <q-list style="width: 100%">
                  <q-item style="padding-left: 0px">
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="french"
                        label="French"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="chinese"
                        label="Chinese"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="jpan"
                        label="Japanese"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                  </q-item>
                  <q-item style="padding-left: 0px">
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="italian"
                        label="Italian"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="greek"
                        label="Greek"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="indian"
                        label="Indian"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                  </q-item>
                  <q-item style="padding-left: 0px">
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="spain"
                        label="Spanish"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="lebanan"
                        label="Lebanese"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="moroccan"
                        label="Moroccan"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                  </q-item>
                  <q-item style="padding-left: 0px">
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="turkish"
                        label="Turkish"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section>
                      <q-checkbox
                        dense
                        v-model="thai"
                        label="Thai"
                        color="primary"
                        style="margin-left: 0px; margin-right: 26px"
                      />
                    </q-item-section>
                    <q-item-section> </q-item-section>
                  </q-item>
                </q-list>
              </div>
            </div>
          </div>
          <div>
            <q-btn label="Submit" type="submit" color="primary" />
            <q-btn
              label="Reset"
              type="reset"
              color="primary"
              flat
              class="q-ml-sm"
            />
          </div>
        </q-form>
      </q-card>
      <!-- </div> -->
    </q-dialog>
    <q-dialog v-model="priceDialog" :position="positionPrice">
      <q-card style="width: 350px"
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
              <q-item-label>Remove constraiant</q-item-label>
            </q-item-section>
          </q-item>
          <q-separator />
          <q-item
            v-if="getRange() !== 'Economic'"
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
            v-if="getRange() !== 'Mid-range'"
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
            v-if="getRange() !== 'Expensive'"
            clickable
            v-close-popup
            @click="price('exp')"
            ><q-item-section avatar>
              <q-avatar icon="trending_up" color="primary" text-color="white" />
            </q-item-section>
            <q-item-section>
              <q-item-label>Expensive Restaurants</q-item-label>
            </q-item-section>
          </q-item>
        </q-list></q-card
      >
    </q-dialog>
    <div v-if="menuValidity && sizeValidity && qualityValidity">
      <div style="width: 100%">
        <q-banner
          dense
          class="bg-green text-white"
          style="margin: 6px 0px 0px 0px"
        >
          <div class="parent">General Settings</div>
        </q-banner>
      </div>
      <q-radio
        v-model="explanationtype"
        checked-icon="task_alt"
        unchecked-icon="panorama_fish_eye"
        val="size"
        label="Show the number of restaurants"
        style="padding-top: 0px; padding-bottom: 0px"
      />
      <div></div>
      <q-radio
        v-model="explanationtype"
        checked-icon="task_alt"
        unchecked-icon="panorama_fish_eye"
        val="quality"
        label="Show the number of high quality restaurants"
        style="padding-top: 0px; padding-bottom: 0px"
      />
      <q-separator />
      <div style="padding: 6px 16px 6px 16px">
        <div v-if="Object.values(this.memberPreference).flat(1).length === 0">
          Add group member preferences to get the number of restaurants
        </div>
        <div v-else>
          <div v-if="explanationtype === 'size'">
            Number of restaurant that will satisfy the group:
            <strong>{{ current }}</strong>
          </div>
          <div v-else>
            Number of restaurant that will satisfy the group:
            <strong>{{ highQuality }}</strong>
          </div>
        </div>
      </div>

      <div style="padding: 6px 16px 6px 16px">
        <div v-if="Object.values(this.memberPreference).flat(1).length > 0">
          <q-separator />
          <div v-if="explanationtype === 'size'">
            For increasing the number of restaurants you need to add new
            preference(s) for
            <strong>
              {{
                groupInfo[
                  String(
                    Object.keys(limitingmembers).reduce(function (a, b) {
                      return limitingmembers[a] > limitingmembers[b] ? a : b;
                    })
                  )
                ][1] === "Organizer"
                  ? "yourself"
                  : groupInfo[
                      String(
                        Object.keys(limitingmembers).reduce(function (a, b) {
                          return limitingmembers[a] > limitingmembers[b]
                            ? a
                            : b;
                        })
                      )
                    ][1]
              }}</strong
            >.
          </div>
          <div v-else>
            For increasing the number of restaurants you need to add new
            preference(s) for
            <strong>
              {{
                groupInfo[
                  String(
                    Object.keys(limitingmembers).reduce(function (a, b) {
                      return limitingmembers[a] > limitingmembers[b] ? a : b;
                    })
                  )
                ][1]
              }}</strong
            >.
          </div>
        </div>
      </div>
    </div>
    <div v-if="menuValidity && sizeValidity && qualityValidity">
      <div
        v-if="userPreferenceList.length > 0"
        class="row no-wrap"
        style="overflow-y: auto"
      >
        <div>
          <div class="row no-wrap">
            <!-- <div v-if="critiqueRange !== ''" @click="openPriceCritique()">
              <q-chip square color="blue" text-color="white">
                {{ getRange() }}
              </q-chip>
            </div> -->
            <!-- <div
            v-for="userInfoList in userPreferenceList"
            :key="userInfoList[1]"
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
          <q-separator /> -->
          </div>
        </div>
      </div>
      <!-- <div v-else class="row no-wrap" style="overflow-y: auto">
        <div v-if="critiqueRange !== ''" @click="openPriceCritique()">
          <q-chip square color="blue" text-color="white">
            {{ getRange() }}
          </q-chip>
        </div>
      </div> -->
      <q-separator />
      <div v-show="!groupActive">
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
        <q-dialog v-if="emptyInfoCheck" v-model="infoEmptyConfirm" persistent>
          <q-card>
            <q-card-section class="row items-center" align="left">
              <q-avatar
                icon="perm_identity"
                :color="userColor"
                text-color="white"
              />
              <span class="q-ml-sm"
                >You have not provided any information. In this case, we can
                only suggest you the most popular preferences. Choose one of the
                following actions.</span
              >
            </q-card-section>

            <q-card-actions align="left">
              <q-btn flat label="Add info" color="primary" v-close-popup />
              <q-btn
                flat
                label="Get Pops"
                color="primary"
                v-close-popup
                v-if="deletePossible"
                @click="popDishes()"
              />
            </q-card-actions>
          </q-card>
        </q-dialog>
        <div v-if="Object.keys(this.organizerId).length">
          <div style="width: 100%">
            <q-banner dense class="bg-green text-white" style="margin: 0px">
              <div class="parent">Group members' Info</div>
            </q-banner>
          </div>
        </div>
        <q-separator v-if="Object.keys(this.organizerId).length" />
        <q-expansion-item
          v-if="Object.keys(this.organizerId).length"
          separator
          style="padding-left: 16px"
        >
          <template v-slot:header>
            <q-item-section avatar>
              <q-icon color="primary" name="group" size="30px" />
            </q-item-section>

            <q-item-section> Group members' Info </q-item-section>
          </template>

          <div
            v-if="
              typeof membersInfo === 'object' &&
              Object.keys(membersInfo).length > 0
            "
          >
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
                      <q-icon name="account_circle" color="green" size="xxs" />
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
                      <q-icon name="flag" color="green" size="xxs" />
                    </q-item-section>
                    <q-item-section style="padding-right: 0px">
                      Nationality
                    </q-item-section>
                    <q-item-section style="padding-right: 0px">
                      {{ member["nationality"] }}
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
                      <q-icon v-else name="woman_2" color="green" size="xxs" />
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
                <q-item>
                  <q-item-section>
                    <q-btn
                      v-if="!addedMember.includes(member_id)"
                      color="primary"
                      label="ADD"
                      style="
                        width: 80px;
                        margin-left: auto;
                        margin-right: 0;
                        float: right;
                      "
                      @click="
                        addNewExtractedMember(
                          member['name'],
                          member['preference'],
                          member_id,
                          member['cuisine'],
                          member['age'],
                          member['gender'],
                          member['nationality']
                        )
                      "
                    />
                  </q-item-section>
                </q-item>
              </div>
            </q-card>
          </div>
          <div v-else>
            <q-card class="my-card" style="width: 100%; padding: 0px" bordered>
              <div class="q-pa-md q-gutter-md">
                <q-list bordered class="rounded-borders" separator>
                  <q-item style="padding-left: 6px; padding-right: 0px">
                    <q-item-section avatar>
                      <q-icon name="pending" color="yellow" size="xxs" />
                    </q-item-section>
                    <q-item-section style="padding-right: 0px">
                      There is not enough members to construct your group.
                      Please wait
                    </q-item-section>
                  </q-item>
                </q-list>
              </div></q-card
            >
          </div>
        </q-expansion-item>
        <q-separator v-if="Object.keys(this.organizerId).length" />
        <div class="parent">
          <div style="width: 100%">
            <q-banner dense class="bg-green text-white" style="margin: 0px">
              <div class="parent">Your group members' profiles</div>
            </q-banner>
          </div>
        </div>
        <q-expansion-item style="padding: 0px 0px 0px 0px">
          <template v-slot:header>
            <q-item-section avatar style="padding: 0px 16px">
              <q-icon color="primary" name="groups" size="30px" />
            </q-item-section>

            <q-item-section style="padding: 0px 16px">
              Group management
            </q-item-section>
          </template>
          <q-list
            bordered
            class="rounded-borders"
            style="max-width: 100%; margin-top: 2px; padding: 6px"
          >
            <div
              v-for="(value, name, index) in groupMembers"
              :key="name"
              style="width: 100%"
            >
              <q-separator v-if="index > 0" />
              <q-item class="memberList">
                <q-item-section avatar top>
                  <q-icon
                    name="perm_identity"
                    :color="value[0] === 'organizer' ? 'blue' : value[0]"
                    size="34px"
                  />
                </q-item-section>
                <q-item-section top>
                  <div v-show="!editableForm[index]" @click="editMember(index)">
                    <q-item-label lines="1">
                      <span class="text-weight-medium">{{
                        value[1] === "Organizer" ? "Me" : value[1]
                      }}</span>
                    </q-item-label>
                    <q-item-label caption lines="1">
                      Role:
                      {{
                        value[0] === "organizer" ? "Organizer" : "Companion"
                      }}</q-item-label
                    >
                  </div>
                  <div v-show="editableForm[index]">
                    <q-input
                      v-model="editText"
                      ref="input"
                      :label="
                        value[1] === 'Organizer'
                          ? 'Current name Me'
                          : 'Current name ' + value[1]
                      "
                      placeholder="Enter new name"
                      dense="dense"
                      @keyup.enter="updateUser(name, index)"
                    />
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
                      v-if="editableVisibility[index] && editedLock === -1"
                      size="12px"
                      flat
                      round
                      icon="edit"
                      @click="editMember(index)"
                    />
                    <!-- <q-btn
                  v-else-if="editableVisibility[index] && editedLock !== -1"
                  size="12px"
                  flat
                  round
                  icon="edit"
                  :color="index === editedLock ? 'black' : 'grey'"
                  @click="index === editedLock ? editMember(index) : ''"
                /> -->
                    <div
                      v-if="!editableVisibility[index] && editedLock !== -1"
                      style="padding-top: 16px"
                    >
                      <q-btn
                        v-if="editText.length > 0"
                        size="12px"
                        flat
                        round
                        icon="done"
                        color="green"
                        @click="updateUser(name, index)"
                      />
                      <q-btn
                        size="12px"
                        flat
                        round
                        icon="cancel"
                        @click="removeEditable(index)"
                      />
                    </div>
                    <q-btn
                      v-if="value[0] !== 'organizer' && !editableForm[index]"
                      size="12px"
                      flat
                      round
                      icon="delete"
                      @click="deleteUser(name, index, value[1])"
                    />
                  </div>
                </q-item-section>
              </q-item>
              <div
                v-if="Object.values(userPreferenceList).flat(1).includes(name)"
                style="margin-left: 65px"
              >
                <div
                  v-for="userInfoList in userPreferenceList"
                  :key="userInfoList[1]"
                  style="display: inline-block; padding-bottom: 6px"
                >
                  <!-- <q-item v-if="userPreferenceList.length > 0"> -->
                  <div v-if="userInfoList[1] === name">
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

                  <!-- </q-item> -->
                </div>
                <q-separator style="margin: 8px 0px"></q-separator>
                <div
                  v-if="
                    typeof memberPreference[name] !== undefined &&
                    memberPreference[name][0].length > 0
                  "
                >
                  <span v-if="explanationtype === 'size'">
                    Number of available restaurant for
                    {{ value[1] === "Organizer" ? "me" : value[1] }}:
                    {{ getUserAvilability(this.memberPreference[name]) }}</span
                  >
                  <span v-else>
                    Number of available high quality restaurant for
                    {{ value[1] }}:
                    {{ getUserAvilabilityQuality(this.memberPreference[name]) }}
                  </span>
                </div>
              </div>
              <q-separator
                style="margin-left: 58px; margin-right: 16px; margin-top: 8px"
              />

              <q-item-section>
                <q-expansion-item
                  icon="settings"
                  label="Add food preferences that this member may like"
                  expand-separator
                  style="margin-left: 58px"
                >
                  <q-card>
                    <q-separator
                      style="margin-left: 58px; margin-right: 16px"
                    />
                    <div
                      v-if="value[1] === 'Organizer'"
                      style="
                        margin-left: 71px;
                        margin-right: 16px;
                        padding-top: 16px;
                      "
                    >
                      Add the food preferences that you may like
                    </div>
                    <div
                      v-else
                      style="
                        margin-left: 71px;
                        margin-right: 16px;
                        padding-top: 16px;
                      "
                    >
                      Add the food preferences that {{ value[1] }} may like
                    </div>
                    <div
                      style="
                        margin-left: 71px;
                        margin-right: 16px;
                        padding-top: 6px;
                        padding-bottom: 6px;
                      "
                    ></div>
                    <q-separator
                      style="
                        margin-left: 71px;
                        margin-right: 16px;
                        margin-bottom: 8px;
                      "
                    />
                    <div
                      style="
                        margin-left: 60px;
                        margin-right: 16px;
                        margin-bottom: 8px;
                      "
                    >
                      <q-radio
                        v-if="preferenceExpansion || preferenceContradiction"
                        v-model="suggestionType"
                        checked-icon="task_alt"
                        unchecked-icon="panorama_fish_eye"
                        val="none"
                        label="No Preference suggestion"
                        style="padding-top: 0px; padding-bottom: 0px"
                      />
                      <q-radio
                        v-if="preferenceExpansion && value[0] !== 'organizer'"
                        v-model="suggestionType"
                        checked-icon="task_alt"
                        unchecked-icon="panorama_fish_eye"
                        val="minfo"
                        :label="
                          value[0] !== 'organizer'
                            ? 'Suggestion based on member info'
                            : 'Suggestion based on member info. (Not active for you)'
                        "
                        :disable="value[0] === 'organizer'"
                        :style="
                          value[0] !== 'organizer'
                            ? [
                                {
                                  'padding-top': '0px',
                                  'padding-bottom': '0px',
                                  'padding-top': '0px',
                                },
                              ]
                            : [
                                {
                                  'padding-top': '0px',
                                  'padding-bottom': '0px',
                                  'padding-top': '0px',
                                  opacity: 0.5,
                                },
                              ]
                        "
                      />
                      <div
                        v-if="suggestionType == 'minfo'"
                        style="
                          margin-left: 40px;
                          margin-right: 16px;
                          margin-bottom: 0px;
                        "
                      >
                        <p
                          @click="popDishes(name)"
                          style="padding: 0px; margin: 0px"
                        >
                          <strong style="color: blue">
                            Popular preferences</strong
                          >
                        </p>
                        <p
                          @click="getInfo(value[1], name)"
                          style="padding: 0px; margin: 0px"
                        >
                          <strong style="color: blue">
                            Predict preferences</strong
                          >
                        </p>
                      </div>

                      <q-radio
                        v-if="preferenceContradiction"
                        v-model="suggestionType"
                        checked-icon="task_alt"
                        unchecked-icon="panorama_fish_eye"
                        val="mprefs"
                        :label="
                          memberPreference[name].length !== 0
                            ? 'Preferences for more restaurants'
                            : 'Preferences for more restaurants. (To activate, insert some preferences for this member)'
                        "
                        :disable="this.memberPreference[name].length === 0"
                        :style="
                          this.memberPreference[name].length !== 0
                            ? [
                                {
                                  'padding-top': '0px',
                                  'padding-bottom': '0px',
                                  'padding-top': '0px',
                                },
                              ]
                            : [
                                {
                                  'padding-top': '0px',
                                  'padding-bottom': '0px',
                                  'padding-top': '0px',
                                  opacity: 0.5,
                                },
                              ]
                        "
                        @click="getContradiction(name)"
                      />
                    </div>
                    <div
                      class="q-pa-md row items-start q-gutter-md"
                      style="margin-left: 40px; padding-top: 0px"
                    >
                      <div
                        v-for="(food, indexInner) in foodsCategory"
                        :key="indexInner"
                      >
                        <!-- {{ cantradictExpansionObj[name] }} -->

                        <q-card
                          :class="
                            explanationtype === 'size'
                              ? isInArray(food, memberPreference[name])
                                ? categoryCardColor[index + 1]
                                : restCategorySize[name][food] === 0
                                ? categoryCardColor[0]
                                : restCategorySize[name][food] < 4
                                ? categoryCardColorIntensity[0]
                                : restCategorySize[name][food] < 6
                                ? categoryCardColorIntensity[1]
                                : categoryCardColorIntensity[2]
                              : isInArray(food, memberPreference[name])
                              ? categoryCardColor[index + 1]
                              : restCategoryQualitySize[name][food] === 0
                              ? categoryCardColor[0]
                              : restCategoryQualitySize[name][food] < 4
                              ? categoryCardColorIntensity[0]
                              : restCategoryQualitySize[name][food] < 6
                              ? categoryCardColorIntensity[1]
                              : categoryCardColorIntensity[2]
                          "
                          @click="addPreferences(name, food, value[1])"
                          :style="
                            suggestionType === 'minfo'
                              ? [
                                  suggestionType == 'minfo' &&
                                  remember[name] !== undefined &&
                                  Object.keys(remember[name])
                                    .filter(function (el) {
                                      return (
                                        memberPreference[name].indexOf(el) < 0
                                      );
                                    })
                                    .splice(0, 2)
                                    .includes(food)
                                    ? {
                                        cursor: 'pointer',
                                        'border-style': 'solid',
                                        'border-width': '0.4em',
                                        'border-color':
                                          groupInfo[name][0] === 'organizer'
                                            ? 'blue'
                                            : groupInfo[name][0],
                                      }
                                    : { cursor: 'pointer' },
                                ]
                              : [
                                  suggestionType == 'mprefs' &&
                                  memberPreference[name] !== undefined &&
                                  expandCotradiction &&
                                  cantradictExpansionObj[String(name)] !==
                                    undefined &&
                                  Object.keys(cantradictExpansionObj[name])
                                    .filter(function (el) {
                                      return (
                                        memberPreference[name].indexOf(el) < 0
                                      );
                                    })
                                    .splice(0, 2)
                                    .includes(food)
                                    ? {
                                        cursor: 'pointer',
                                        'border-style': 'solid',
                                        'border-width': '0.4em',
                                        'border-color':
                                          groupInfo[name][0] === 'organizer'
                                            ? 'blue'
                                            : groupInfo[name][0],
                                      }
                                    : { cursor: 'pointer' },
                                ]
                          "
                        >
                          <q-card-section style="padding: 8px 8px 8px 8px">
                            {{ food_name_change(food) }}
                            <span
                              v-if="
                                typeof memberPreference[name] !== undefined &&
                                !memberPreference[name].includes(food)
                              "
                            >
                              <span v-if="explanationtype === 'size'">
                                ({{ restCategorySize[name][food] }})</span
                              ><span v-else
                                >({{
                                  restCategoryQualitySize[name][food]
                                }})</span
                              ></span
                            >
                          </q-card-section>
                        </q-card>
                      </div>
                    </div></q-card
                  >
                </q-expansion-item>

                <!-- <q-separator
                  v-if="
                    revisionTriggre ||
                    (!revisionTriggre && value[0] !== 'organizer') ||
                    (explanationtype === 'size' && current < 5) ||
                    (explanationtype === 'quality' && highQuality < 5)
                  "
                  style="margin-left: 58px; margin-right: 16px"
                /> -->
                <!-- <q-expansion-item
                  v-if="
                    revisionTriggre ||
                    (!revisionTriggre && value[0] !== 'organizer') ||
                    (explanationtype === 'size' && current < 5) ||
                    (explanationtype === 'quality' && highQuality < 5)
                  "
                  v-model="expanded[index]"
                  icon="settings"
                  label="Preference Expansion"
                  style="margin-left: 58px"
                >
                  <q-card>
                    <div style="margin-left: 36px; padding-top: 0px">
                      <div style="margin-left: 16px">
                        <q-separator
                          style="
                            margin-right: 32px;
                            margin-bottom: 16px;
                            margin-left: 16px;
                          "
                        />
                        <q-expansion-item
                          v-if="value[0] !== 'organizer'"
                          :header-inset-level="0"
                          icon="support"
                          label="Preference Suggestion"
                        >
                          <div
                            style="
                              margin-left: 16px;
                              margin-right: 16px;
                              align: justify;
                            "
                          >
                            Do you need help for expanding
                            <strong>{{ value[1] }}</strong> preferences?
                            <p
                              v-if="Object.keys(remember).includes(name)"
                              style="align: justify; margin-top: 6px"
                            >
                              Based on the provided information,
                              {{ value[1] }} may like one of the following
                              dishes. Click on them to add to
                              {{ value[1] }} favorit dishes list.
                            </p>

                            <p @click="getInfo(value[1], name)">
                              <strong style="color: blue">
                                click here to insert or revise info</strong
                              >
                            </p>
                            <div
                              v-if="Object.keys(remember).includes(name)"
                              class="q-pa-md row items-start"
                              style="padding-left: 0px; margin-left: 0px"
                            >
                              <span style="visibility: hidden">{{
                                (counterLoop = 0)
                              }}</span>
                              <span
                                v-for="(itemPref, index) in Object.keys(
                                  remember[name]
                                )"
                                :key="index"
                              >
                                <div
                                  v-if="
                                    counterLoop <= 1 &&
                                    foodsCategory.includes(
                                      Object.keys(remember[name])[index]
                                    ) &&
                                    memberPreference[name] != null &&
                                    !memberPreference[name].includes(
                                      Object.keys(remember[name])[index]
                                    )
                                  "
                                  style="
                                    float: left;
                                    padding-left: 0px;
                                    margin-left: 0px;
                                  "
                                >
                                  <div>
                                    <q-card
                                      @click="
                                        addPreferences(
                                          name,
                                          Object.keys(remember[name])[index],
                                          value[1]
                                        )
                                      "
                                      style="cursor: pointer; margin-right: 6px"
                                    >
                                      <q-card
                                        :class="
                                          explanationtype === 'size'
                                            ? isInArray(
                                                Object.keys(remember[name])[
                                                  index
                                                ],
                                                memberPreference[name]
                                              )
                                              ? categoryCardColor[index + 1]
                                              : restCategorySize[name][
                                                  Object.keys(remember[name])[
                                                    index
                                                  ]
                                                ] === 0
                                              ? categoryCardColor[0]
                                              : restCategorySize[name][
                                                  Object.keys(remember[name])[
                                                    index
                                                  ]
                                                ] < 4
                                              ? categoryCardColorIntensity[0]
                                              : restCategorySize[name][
                                                  Object.keys(remember[name])[
                                                    index
                                                  ]
                                                ] < 6
                                              ? categoryCardColorIntensity[1]
                                              : categoryCardColorIntensity[2]
                                            : isInArray(
                                                Object.keys(remember[name])[
                                                  index
                                                ],
                                                memberPreference[name]
                                              )
                                            ? categoryCardColor[index + 1]
                                            : restCategoryQualitySize[name][
                                                Object.keys(remember[name])[
                                                  index
                                                ]
                                              ] === 0
                                            ? categoryCardColor[0]
                                            : restCategoryQualitySize[name][
                                                Object.keys(remember[name])[
                                                  index
                                                ]
                                              ] < 4
                                            ? categoryCardColorIntensity[0]
                                            : restCategoryQualitySize[name][
                                                Object.keys(remember[name])[
                                                  index
                                                ]
                                              ] < 6
                                            ? categoryCardColorIntensity[1]
                                            : categoryCardColorIntensity[2]
                                        "
                                        style="cursor: pointer"
                                      >
                                        <q-card-section
                                          style="padding: 8px 8px 8px 8px"
                                        >
                                          {{
                                            food_name_change(
                                              Object.keys(remember[name])[index]
                                            )
                                          }}
                                          <span
                                            v-if="
                                              typeof this.memberPreference[
                                                name
                                              ] !== undefined &&
                                              !this.memberPreference[
                                                name
                                              ].includes(
                                                Object.keys(remember[name])[
                                                  index
                                                ]
                                              )
                                            "
                                          >
                                            <span
                                              v-if="explanationtype === 'size'"
                                            >
                                              ({{
                                                restCategorySize[name][
                                                  Object.keys(remember[name])[
                                                    index
                                                  ]
                                                ]
                                              }})</span
                                            ><span v-else
                                              >({{
                                                restCategoryQualitySize[name][
                                                  Object.keys(remember[name])[
                                                    index
                                                  ]
                                                ]
                                              }})</span
                                            ></span
                                          >
                                        </q-card-section>
                                      </q-card>
                                    </q-card>
                                    <span style="visibility: hidden">
                                      {{ counterLoop++ }}
                                    </span>
                                  </div>
                                </div>
                              </span>
                              <div v-if="counterLoop === 0">
                                Sorry but no more food is available to recommend
                                you.
                              </div>
                            </div>
                          </div>
                        </q-expansion-item>
                      </div>
                    </div>

                    <div style="margin-left: 36px; padding-top: 0px">
                      <div
                        v-if="
                          revisionTriggre ||
                          (explanationtype === 'size' && current < 5) ||
                          (explanationtype === 'quality' && highQuality < 5)
                        "
                        style="margin-left: 0px"
                      >
                        {{ getContradiction() }}
                        <q-expansion-item
                          v-if="
                            typeof memberPreference[name] === 'object' &&
                            memberPreference[name].length != 0
                          "
                          :header-inset-level="0"
                          icon="published_with_changes"
                          label="Contradiction Resolution"
                          style="margin-left: 16px"
                        >
                          <div
                            style="
                              margin-left: 16px;
                              margin-right: 16px;
                              align: justify;
                            "
                          >
                            To remove contradiction you need to expand
                            {{ value[1] }} preferences. {{ value[1] }} may like
                            the following dishes.
                            <div
                              class="q-pa-md row items-start"
                              style="padding-left: 0px; margin-left: 0px"
                            >
                              <span style="visibility: hidden">{{
                                (counterLoop = 0)
                              }}</span>
                              <div
                                v-for="(
                                  objKey, objValue, index
                                ) in cantradictExpansionObj[String(name)]"
                                :key="index"
                              >
                                <span
                                  v-if="
                                    counterLoop <= 2 &&
                                    foodsCategory.includes(objValue) &&
                                    memberPreference[name] != null &&
                                    !memberPreference[name].includes(objValue)
                                  "
                                >
                                  <div>
                                    <div>
                                      <div>
                                        <q-card
                                          @click="
                                            addPreferences(
                                              name,
                                              objValue,
                                              value[1]
                                            )
                                          "
                                          style="
                                            cursor: pointer;
                                            margin-right: 6px;
                                          "
                                        >
                                          <q-card
                                            :class="
                                              explanationtype === 'size'
                                                ? isInArray(
                                                    objValue,
                                                    memberPreference[name]
                                                  )
                                                  ? categoryCardColor[index + 1]
                                                  : restCategorySize[name][
                                                      objValue
                                                    ] === 0
                                                  ? categoryCardColor[0]
                                                  : restCategorySize[name][
                                                      objValue
                                                    ] < 4
                                                  ? categoryCardColorIntensity[0]
                                                  : restCategorySize[name][
                                                      objValue
                                                    ] < 6
                                                  ? categoryCardColorIntensity[1]
                                                  : categoryCardColorIntensity[2]
                                                : isInArray(
                                                    objValue,
                                                    memberPreference[name]
                                                  )
                                                ? categoryCardColor[index + 1]
                                                : restCategoryQualitySize[name][
                                                    objValue
                                                  ] === 0
                                                ? categoryCardColor[0]
                                                : restCategoryQualitySize[name][
                                                    objValue
                                                  ] < 4
                                                ? categoryCardColorIntensity[0]
                                                : restCategoryQualitySize[name][
                                                    objValue
                                                  ] < 6
                                                ? categoryCardColorIntensity[1]
                                                : categoryCardColorIntensity[2]
                                            "
                                            style="cursor: pointer"
                                          >
                                            <q-card-section
                                              style="padding: 8px 8px 8px 8px"
                                            >
                                              {{ food_name_change(objValue) }}
                                              <span
                                                v-if="
                                                  typeof this.memberPreference[
                                                    name
                                                  ] !== undefined &&
                                                  !this.memberPreference[
                                                    name
                                                  ].includes(objValue)
                                                "
                                              >
                                                <span
                                                  v-if="
                                                    explanationtype === 'size'
                                                  "
                                                >
                                                  ({{
                                                    restCategorySize[name][
                                                      objValue
                                                    ]
                                                  }})</span
                                                ><span v-else
                                                  >({{
                                                    restCategoryQualitySize[
                                                      name
                                                    ][objValue]
                                                  }})</span
                                                ></span
                                              >
                                            </q-card-section>
                                          </q-card>
                                        </q-card>
                                        <span style="visibility: hidden">
                                          {{ counterLoop++ }}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                  <span style="visibility: hidden">
                                    {{ counterLoop++ }}
                                  </span>
                                </span>
                              </div>
                              <div v-if="counterLoop === 0">
                                Sorry but no more food is available to recommend
                                you.
                              </div>
                            </div>
                          </div>
                        </q-expansion-item>
                        <q-separator
                          style="
                            margin-right: 32px;
                            margin-bottom: 16px;
                            margin-left: 15px;
                          "
                        />
                      </div>
                    </div>
                  </q-card>
                  <div
                    style="
                      align-items: right;
                      margin-bottom: 16px;
                      padding-right: 16px;
                      display: flex;
                      justify-content: right;
                    "
                  >
                    <q-btn
                      size="xs"
                      round
                      @click="closeExpand(index)"
                      color="grey"
                      icon="expand_less"
                    ></q-btn>
                  </div>
                </q-expansion-item> -->
              </q-item-section>
            </div>
          </q-list>
          <div v-if="memberCounter > 1" class="groupInfoText">
            <div>
              <q-input
                dense
                filled
                bottom-slots
                v-model="memberName"
                label="Name of new member"
                class="inputBox"
              >
                <template v-slot:hint>
                  <p>
                    Max number of friends to add 4, remained
                    {{ memberCounter - 1 }}.
                  </p>
                </template>
                <template v-slot:after>
                  <q-btn
                    label="ADD MEMBER"
                    color="primary"
                    @click="submitUser(memberCounter)"
                  />
                </template>
              </q-input>
            </div>
          </div>
        </q-expansion-item>

        <!-- <div class="parent">
        <q-card-section>
          <q-btn
            color="primary"
            label="ADD LOCATION"
            icon="map"
            @click="determinePage('map')"
            class="critique-btn"
          />
        </q-card-section>
      </div> -->
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
    <!-- <div v-show="!mapActive" class="scroll">
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
    </div> -->
    <!-- <div v-show="!prefActive">
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
                      <q-card-section>
                        {{ food_name_change(food) }}
                      </q-card-section>
                    </q-card>
                  </div>
                </div>
              </q-card>
            </q-expansion-item>
          </q-list>
        </div>
      </div>
    </div> -->
  </div>
  <!-- <div v-show="endOfSession">
    <div class="no-tasks absolute-center text-h5 text-primary text-center">
      Thank you for participating in our user study. For starting a new session
      just click on the following button:
      <q-btn @click="newSessoin()">New Session</q-btn>
    </div>
  </div> -->
</template>

<script>
import { markRaw } from "vue";
import axios from "axios";
import { ref } from "vue";
import VueGeolocation from "vue-browser-geolocation";
export default {
  props: [
    "groupInfo",
    "organizerId",
    "critiqueRange",
    "revisionTriggre",
    "stepSend",
    "revisionSizeRecieved",
  ],
  emits: [
    "groupConstructed",
    "userPreferenceList",
    "critiqueIssued",
    "currentRestaurants",
  ],
  data() {
    return {
      disclimer: true,
      revisionSize: this.revisionSizeRecieved,
      suggestionType: ref("none"),
      limitingmembersQualiry: {},
      limitingmembers: {},
      current: 0,
      highQuality: 0,
      explanationtype: ref("size"),
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
      preferenceContradiction: true,
      preferenceExpansion: true,
      suggestionActivatedPop: false,
      menuValidity: false,
      qualityValidity: false,
      sizeValidity: false,
      revisionBannerToggle: true,
      expandCotradiction: false,
      emptyInfoCheck: false,
      infoEmptyConfirm: "",
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
      genderModel: ref(null),
      genderOption: ["Female", "Male"],
      countryModel: ref(null),
      countryOption: [
        "Afghanistan",
        "Albania",
        "Algeria",
        "American Samoa",
        "Andorra",
        "Angola",
        "Anguilla",
        "Antarctica",
        "Antigua and Barbuda",
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
        "Bolivia (Plurinational State of)",
        "Bonaire, Sint Eustatius and Saba",
        "Bosnia and Herzegovina",
        "Botswana",
        "Bouvet Island",
        "Brazil",
        "British Indian Ocean Territory (the)",
        "Brunei Darussalam",
        "Bulgaria",
        "Burkina Faso",
        "Burundi",
        "Cabo Verde",
        "Cambodia",
        "Cameroon",
        "Canada",
        "Cayman Islands (the)",
        "Central African Republic (the)",
        "Chad",
        "Chile",
        "China",
        "Christmas Island",
        "Cocos (Keeling) Islands (the)",
        "Colombia",
        "Comoros (the)",
        "Congo (the Democratic Republic of the)",
        "Congo (the)",
        "Cook Islands (the)",
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
        "Dominican Republic (the)",
        "Ecuador",
        "Egypt",
        "El Salvador",
        "Equatorial Guinea",
        "Eritrea",
        "Estonia",
        "Eswatini",
        "Ethiopia",
        "Falkland Islands (the) [Malvinas]",
        "Faroe Islands (the)",
        "Fiji",
        "Finland",
        "France",
        "French Guiana",
        "French Polynesia",
        "French Southern Territories (the)",
        "Gabon",
        "Gambia (the)",
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
        "Heard Island and McDonald Islands",
        "Holy See (the)",
        "Honduras",
        "Hong Kong",
        "Hungary",
        "Iceland",
        "India",
        "Indonesia",
        "Iran (Islamic Republic of)",
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
        "Korea (the Democratic People's Republic of)",
        "Korea (the Republic of)",
        "Kuwait",
        "Kyrgyzstan",
        "Lao People's Democratic Republic (the)",
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
        "Marshall Islands (the)",
        "Martinique",
        "Mauritania",
        "Mauritius",
        "Mayotte",
        "Mexico",
        "Micronesia (Federated States of)",
        "Moldova (the Republic of)",
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
        "Netherlands (the)",
        "New Caledonia",
        "New Zealand",
        "Nicaragua",
        "Niger (the)",
        "Nigeria",
        "Niue",
        "Norfolk Island",
        "Northern Mariana Islands (the)",
        "Norway",
        "Oman",
        "Pakistan",
        "Palau",
        "Palestine, State of",
        "Panama",
        "Papua New Guinea",
        "Paraguay",
        "Peru",
        "Philippines (the)",
        "Pitcairn",
        "Poland",
        "Portugal",
        "Puerto Rico",
        "Qatar",
        "Republic of North Macedonia",
        "Romania",
        "Russian Federation (the)",
        "Rwanda",
        "Réunion",
        "Saint Barthélemy",
        "Saint Helena, Ascension and Tristan da Cunha",
        "Saint Kitts and Nevis",
        "Saint Lucia",
        "Saint Martin (French part)",
        "Saint Pierre and Miquelon",
        "Saint Vincent and the Grenadines",
        "Samoa",
        "San Marino",
        "Sao Tome and Principe",
        "Saudi Arabia",
        "Senegal",
        "Serbia",
        "Seychelles",
        "Sierra Leone",
        "Singapore",
        "Sint Maarten (Dutch part)",
        "Slovakia",
        "Slovenia",
        "Solomon Islands",
        "Somalia",
        "South Africa",
        "South Georgia and the South Sandwich Islands",
        "South Sudan",
        "Spain",
        "Sri Lanka",
        "Sudan (the)",
        "Suriname",
        "Svalbard and Jan Mayen",
        "Sweden",
        "Switzerland",
        "Syrian Arab Republic",
        "Taiwan",
        "Tajikistan",
        "Tanzania, United Republic of",
        "Thailand",
        "Timor-Leste",
        "Togo",
        "Tokelau",
        "Tonga",
        "Trinidad and Tobago",
        "Tunisia",
        "Turkey",
        "Turkmenistan",
        "Turks and Caicos Islands (the)",
        "Tuvalu",
        "Uganda",
        "Ukraine",
        "United Arab Emirates (the)",
        "United Kingdom of Great Britain and Northern Ireland (the)",
        "United States Minor Outlying Islands (the)",
        "United States of America (the)",
        "Uruguay",
        "Uzbekistan",
        "Vanuatu",
        "Venezuela (Bolivarian Republic of)",
        "Viet Nam",
        "Virgin Islands (British)",
        "Virgin Islands (U.S.)",
        "Wallis and Futuna",
        "Western Sahara",
        "Yemen",
        "Zambia",
        "Zimbabwe",
        "Åland Islands",
      ],
      nationality: this.countryModel,
      memberNameInfo: "none",
      memberAgeInfo: 0,
      expanded: [false],
      membersInfo: {},
      editedLock: -1,
      options: [],
      searchLabel: "Search for dish",
      searchInput: "",
      foodCategoryObj: require(`../assets/food_category.json`),
      foodCategoryObjDefault: require(`../assets/food_category.json`),
      foodCategoryObjName: [],
      foodCategoryObjNameDefault: [],
      memberPreference: {},
      tempCategoryCardColor: [
        "my-card",
        "my-card bg-blue text-white",
        "my-card bg-purple text-white",
        "my-card bg-orange text-white",
        "my-card bg-red text-white",
        "my-card bg-yellow text-white",
      ],
      categoryCardColorIntensity: [
        "my-card bg-green-4 text-white",
        "my-card bg-green-7 text-white",
        "my-card bg-green-10 text-white",
      ],
      categoryCardColor: ["my-card", "my-card bg-blue text-white"],
      foodsCategory: [
        "PASTA",
        "CARNE",
        "PESCE",
        "RISO",
        "CROSTACEI_E_MOLLUSCHI",
        "PIZZA",
        "VERDURE",
        "GNOCCHI",
        "TORTELLINI",
        "LEGUMI",
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
      userPreferenceList: [],
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
      memberColor: ["purple", "red", "orange", "yellow"],
      memberColordelete: ["blue", "purple", "red", "orange", "yellow"],
      endOfSession: false,
      group_id_intract: JSON.parse(sessionStorage.getItem("group_id")),
      positionPrice: ref("bottom"),
      priceDialog: ref(false),
      infoDialog: ref(false),
      submittedInfo: {},
      memberInfoName: "",
      memberInfoId: -1,
      cantradictExpansionObj: {},
      remember: {},
      restMenu: [],
      restMenuId: {},
      restCategorySize: {},
      restCategoryQualitySize: {},
      addedMember: [],
      membersConnection: {},
    };
  },
  methods: {
    addNewExtractedMember(
      name,
      preferences,
      member_id,
      getCuisine,
      getAge,
      getGender,
      nationality
    ) {
      var url = "http://46.18.25.97:8050/users/companion";
      var request = "POST";
      var user_default = {
        first_name: "Organizer",
        last_name: "string",
        email: "string",
        latitude: 0,
        longitude: 0,
        role: "companion",
        group_id: 0,
      };

      var user_temp_object = user_default;
      var role = this.memberColor.splice(0, 1)[0];
      user_temp_object["first_name"] = name;
      user_temp_object["group_id"] = JSON.parse(
        sessionStorage.getItem("group_id")
      );
      var data = JSON.stringify(user_temp_object);
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
            temp_user_id = JSON.parse(response.data)["user_id"];
            this.setInforStorage(
              temp_user_id,
              name,
              getGender,
              nationality,
              getAge,
              Object.values(preferences),
              Object.values(getCuisine)
            );
            this.membersConnection[temp_user_id] = member_id;
            this.memberName = "";
            sessionStorage.setItem(role, temp_user_id);
            sessionStorage.setItem(role_name, first_name);
            this.groupMembers[temp_user_id] = [role, first_name];
            var temp_element_to_add = {};
            temp_element_to_add["id"] = temp_user_id;
            temp_element_to_add["name"] = first_name;
            temp_element_to_add["show"] = true;
            this.memberPreference[temp_user_id] = [];
            this.qualityValidity = false;
            this.sizeValidity = false;
            if (role === "orange") {
              this.categoryCardColor.push("my-card bg-orange text-white");
            } else if (role === "purple") {
              this.categoryCardColor.push("my-card bg-purple text-white");
            } else if (role === "red") {
              this.categoryCardColor.push("my-card bg-red text-white");
            } else {
              this.categoryCardColor.push("my-card bg-yellow text-white");
            }
            for (var dish of preferences) {
              this.addPreferences(String(temp_user_id), dish, "name");
            }
            this.getMenu();
          });
      }
      this.memberCounter = this.memberCounter - 1;
      this.addedMember.push(member_id);
      this.editableVisibility.push(true);
      this.editableForm.push(false);
      this.expanded.push(false);
    },
    popDishes(receivedId) {
      var usrId = 0;
      for (var [key, value] of Object.entries(this.groupInfo)) {
        if (value[0] === "organizer") {
          usrId = key;
        }
      }
      var remeberingInteraction = {
        user_id: usrId,
        group_id: this.group_id_intract,
        remembring_pop: true,
        remembring_detialed: false,
        remebr_user_id: receivedId,
      };
      axios
        .post(
          "http://46.18.25.97:8050/interaction/remebring/storage",
          remeberingInteraction
        )
        .then();
      this.$q.loading.show();
      this.memberInfoId = receivedId;
      axios
        .get("http://46.18.25.97:8050/contradiction/remember/pop")
        .then((response) => {
          this.remember[this.memberInfoId] = response.data;
          this.$q.loading.hide();
          this.suggestionActivatedPop = true;
          this.emptyInfoCheck = false;
          this.infoDialog = false;
          if (
            JSON.parse(sessionStorage.getItem("rememberInfo")) === null ||
            (JSON.parse(sessionStorage.getItem("rememberInfo")) !== null &&
              Object.keys(JSON.parse(sessionStorage.getItem("rememberInfo")))
                .length === 0)
          ) {
            sessionStorage.setItem(
              "rememberInfo",
              JSON.stringify(this.remember)
            );
          } else {
            var temp = JSON.parse(sessionStorage.getItem("rememberInfo"));
            sessionStorage.removeItem("rememberInfo");
            sessionStorage.setItem(
              "rememberInfo",
              JSON.stringify(this.remember)
            );
          }
        });
    },
    setInforStorage(id, name, gender, nationality, age, preferences, cuisine) {
      var info = {};
      info["id"] = id;
      info["gender"] = gender;
      info["nationality"] = nationality;
      info["age"] = age;
      info["name"] = name;
      info["PASTA"] = preferences.includes("PASTA");
      info["CARNE"] = preferences.includes("CARNE");
      info["PIZZA"] = preferences.includes("PIZZA");
      info["TORTELLINI"] = preferences.includes("TORTELLINI");
      info["SALUMI"] = preferences.includes("SALUMI");
      info["PESCE"] = preferences.includes("PESCE");
      info["LEGUMI"] = preferences.includes("LEGUMI");
      info["FUNGHI"] = preferences.includes("FUNGHI");
      info["CROSTACEI_E_MOLLUSCHI"] = preferences.includes(
        "CROSTACEI_E_MOLLUSCHI"
      );
      info["VERDURE"] = preferences.includes("VERDURE");
      info["GNOCCHI"] = preferences.includes("GNOCCHI");
      info["INTERIORA"] = preferences.includes("INTERIORA");
      info["FORMAGGI"] = preferences.includes("FORMAGGI");
      info["RISO"] = preferences.includes("RISO");
      info["french"] = cuisine.includes("french");
      info["chinese"] = cuisine.includes("chinese");
      info["jpan"] = cuisine.includes("jpan");
      info["italian"] = cuisine.includes("italian");
      info["greek"] = cuisine.includes("greek");
      info["indian"] = cuisine.includes("indian");
      info["spain"] = cuisine.includes("spain");
      info["lebanan"] = cuisine.includes("lebanan");
      info["moroccan"] = cuisine.includes("moroccan");
      info["turkish"] = cuisine.includes("turkish");
      info["thai"] = cuisine.includes("thai");
      if (
        JSON.parse(sessionStorage.getItem("remember")) === null ||
        (JSON.parse(sessionStorage.getItem("remember")) !== null &&
          Object.keys(JSON.parse(sessionStorage.getItem("remember"))).length ===
            0)
      ) {
        var temp = {};
        temp[id] = info;
        sessionStorage.setItem("remember", JSON.stringify(temp));
      } else {
        var temp = {};
        temp = JSON.parse(sessionStorage.getItem("remember"));
        sessionStorage.removeItem("remember");
        temp[id] = info;
        sessionStorage.setItem("remember", JSON.stringify(temp));
      }
    },
    onSubmitInfo() {
      var usrId = 0;
      for (var [key, value] of Object.entries(this.groupInfo)) {
        if (value[0] === "organizer") {
          usrId = key;
        }
      }
      var remeberingInteraction = {
        user_id: usrId,
        group_id: this.group_id_intract,
        remembring_pop: false,
        remembring_detialed: true,
        remebr_user_id: this.memberInfoId,
      };
      axios
        .post(
          "http://46.18.25.97:8050/interaction/remebring/storage",
          remeberingInteraction
        )
        .then();
      var info = {};
      info["id"] = this.memberInfoId;
      info["gender"] = this.genderModel;
      info["nationality"] = this.countryModel;
      info["age"] = this.memberAgeInfo;
      info["name"] = this.memberInfoName;
      info["PASTA"] =
        this.memberPreference[this.memberInfoId].includes("PASTA");
      info["CARNE"] =
        this.memberPreference[this.memberInfoId].includes("CARNE");
      info["PIZZA"] =
        this.memberPreference[this.memberInfoId].includes("PIZZA");
      info["TORTELLINI"] =
        this.memberPreference[this.memberInfoId].includes("TORTELLINI");
      info["SALUMI"] =
        this.memberPreference[this.memberInfoId].includes("SALUMI");
      info["PESCE"] =
        this.memberPreference[this.memberInfoId].includes("PESCE");
      info["LEGUMI"] =
        this.memberPreference[this.memberInfoId].includes("LEGUMI");
      info["FUNGHI"] =
        this.memberPreference[this.memberInfoId].includes("FUNGHI");
      info["CROSTACEI_E_MOLLUSCHI"] = this.memberPreference[
        this.memberInfoId
      ].includes("CROSTACEI_E_MOLLUSCHI");
      info["VERDURE"] =
        this.memberPreference[this.memberInfoId].includes("VERDURE");
      info["GNOCCHI"] =
        this.memberPreference[this.memberInfoId].includes("GNOCCHI");
      info["INTERIORA"] =
        this.memberPreference[this.memberInfoId].includes("INTERIORA");
      info["FORMAGGI"] =
        this.memberPreference[this.memberInfoId].includes("FORMAGGI");
      info["RISO"] = this.memberPreference[this.memberInfoId].includes("RISO");
      info["french"] = this.french;
      info["chinese"] = this.chinese;
      info["jpan"] = this.jpan;
      info["italian"] = this.italian;
      info["greek"] = this.greek;
      info["indian"] = this.indian;
      info["spain"] = this.spain;
      info["lebanan"] = this.lebanan;
      info["moroccan"] = this.moroccan;
      info["turkish"] = this.turkish;
      info["thai"] = this.thai;
      if (
        this.french ||
        this.chinese ||
        this.jpan ||
        this.italian ||
        this.greek ||
        this.indian ||
        this.spain ||
        this.lebanan ||
        this.moroccan ||
        this.turkish ||
        this.thai ||
        this.memberAgeInfo > 0 ||
        this.genderModel !== null ||
        this.countryModel !== null
      ) {
        this.infoDialog = false;
        this.$q.loading.show();
        axios
          .post("http://46.18.25.97:8050/contradiction/remember/", info)
          .then((response) => {
            this.$q.loading.hide();
            this.remember[this.memberInfoId] = response.data;
            sessionStorage.removeItem("rememberInfo");
            sessionStorage.setItem(
              "rememberInfo",
              JSON.stringify(this.remember)
            );
          });
        if (
          JSON.parse(sessionStorage.getItem("remember")) === null ||
          (JSON.parse(sessionStorage.getItem("remember")) !== null &&
            Object.keys(JSON.parse(sessionStorage.getItem("remember")))
              .length === 0)
        ) {
          var temp = {};
          temp[this.memberInfoId] = info;
          sessionStorage.setItem("remember", JSON.stringify(temp));
        } else {
          var temp = {};
          temp = JSON.parse(sessionStorage.getItem("remember"));
          sessionStorage.removeItem("remember");
          temp[this.memberInfoId] = info;
          sessionStorage.setItem("remember", JSON.stringify(temp));
        }
      } else {
        this.emptyInfoCheck = true;
      }
    },
    onResetInfo() {
      this.french = ref(false);
      this.chinese = ref(false);
      this.jpan = ref(false);
      this.italian = ref(false);
      this.greek = ref(false);
      this.indian = ref(false);
      this.spain = ref(false);
      this.lebanan = ref(false);
      this.moroccan = ref(false);
      this.turkish = ref(false);
      this.thai = ref(false);
      this.genderModel = ref(null);
      this.countryModel = ref(null);
      this.memberNameInfo = "none";
      this.memberAgeInfo = 0;
      var temp = {};
      temp = JSON.parse(sessionStorage.getItem("remember"));
      sessionStorage.removeItem("remember");
      delete temp[this.memberInfoId];
      sessionStorage.setItem("remember", JSON.stringify(temp));
    },
    getInfo(name, uId) {
      if (sessionStorage.getItem("remember") !== null) {
        if (JSON.parse(sessionStorage.getItem("remember"))[uId] !== undefined) {
          var temp = JSON.parse(sessionStorage.getItem("remember"))[uId];
          this.french = temp["french"];
          this.chinese = temp["chinese"];
          this.jpan = temp["jpan"];
          this.italian = temp["italian"];
          this.greek = temp["greek"];
          this.indian = temp["indian"];
          this.spain = temp["spain"];
          this.lebanan = temp["lebanan"];
          this.moroccan = temp["moroccan"];
          this.turkish = temp["turkish"];
          this.thai = temp["thai"];
          this.genderModel = temp["gender"];
          this.countryModel = temp["nationality"];
          this.memberAgeInfo = temp["age"];
        }
      }
      this.infoDialog = true;
      this.memberInfoName = name;
      this.memberInfoId = uId;
    },
    scrollToTop() {
      window.scrollTo(0, 0);
    },
    loadingShow() {
      $q.loading.show();
    },
    loadingHide() {
      $q.loading.hide();
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
        String(this.group_id_intract);
      axios
        .post(url, newPreference, {
          headers: headers,
        })
        .then(() => {
          sessionStorage.setItem("relevanceValidation", false);
          sessionStorage.setItem("attractivenessValidation", false);
          sessionStorage.setItem("SimilarityValidation", false);
        });
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
      } else {
        return "Expensive";
      }
    },
    closeExpand(expandValue) {
      this.expanded[expandValue] = false;
      // expandValue = expandValue + 1;
      // this.expanded[expandValue] = true;
    },
    extractNumberOfFood(userId) {
      var counter = 0;
      for (var userInfoList of this.userPreferenceList) {
        if (userInfoList[1] === userId) {
          counter++;
        }
      }
      return counter;
    },
    newSessoin() {
      location.reload();
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
    cancelDeleting() {
      this.deleteDialog = false;
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Cancel deleting",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
    },
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
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: page,
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
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
      var interactionData = {
        group_id: parseInt(this.group_id_intract),
        interaction: "User submitted",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
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
      // if (this.deletedCount > 0) {
      //   var colorOfNewUser = this.deletedColors.shift();
      //   this.sendRequest(url, request, data, colorOfNewUser, "insert");
      //   this.deletedCount--;
      // } else {
      var uId = this.sendRequest(
        url,
        request,
        data,
        this.memberColor.splice(0, 1)[0],
        "insert"
      );
      this.memberCounter = this.memberCounter - 1;
      this.editableVisibility.push(true);
      this.editableForm.push(false);
      // }
      this.expanded.push(false);
      return uId;
      // this.$q.notify({
      //   message: "New member is added.",
      //   icon: "person",
      //   color: "green",
      // });
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
              this.qualityValidity = false;
              this.sizeValidity = false;
              this.getMenu();
              if (role === "orange") {
                this.categoryCardColor.push("my-card bg-orange text-white");
              } else if (role === "purple") {
                this.categoryCardColor.push("my-card bg-purple text-white");
              } else if (role === "red") {
                this.categoryCardColor.push("my-card bg-red text-white");
              } else {
                this.categoryCardColor.push("my-card bg-yellow text-white");
              }
              return temp_user_id;
            }
          });
      }
    },
    removeEditable(index_in) {
      this.editableForm[index_in] = false;
      this.editableVisibility[index_in] = true;
      this.editedLock = -1;
      this.editText = "";
    },
    editMember(index) {
      this.editedLock = index;
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Member Edited",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      for (var index_in in this.editableForm) {
        this.editableForm[index_in] = false;
        this.editableVisibility[index_in] = true;
      }
      this.editableForm[index] = true;
      this.editableVisibility[index] = false;
      this.$nextTick(() => this.$refs["input"][index].focus());
      // this.$q.notify({
      //   message: "Member information is modified.",
      //   icon: "person",
      //   color: "green",
      // });
    },
    updateUser(userId, index) {
      this.editedLock = -1;
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Update user " + String(userId) + " information",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
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
      if (this.editText.length > 0) {
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
      }
      // this.$q.notify({
      //   message: "Member information is updated.",
      //   icon: "person",
      //   color: "green",
      // });
    },
    deleteUser(userId, index, name) {
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Deleted " + String(userId),
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.deleteDialog = true;
      if (index === 0) {
        this.deleteMassage = "Impossible to delete the organizer of the group.";
        this.deletePossible = false;
        this.userColor = this.groupInfo[userId][0];
        this.deletingId = userId;
      } else {
        this.deleteMassage = "Are you sure you want to delete " + name + "?";
        this.deletePossible = true;
        this.userColor = this.groupInfo[userId][0];
        this.deletingId = userId;
      }
    },

    finishDeleting(color) {
      this.memberCounter++;
      this.deletedCount++;
      if (color === "orange") {
        const index = this.categoryCardColor.indexOf(
          "my-card bg-orange text-white"
        );
        if (index > -1) {
          this.categoryCardColor.splice(index, 1);
        }
        this.memberColor.unshift("orange");
        this.deletedColors.push("orange");
      } else if (color === "purple") {
        const index = this.categoryCardColor.indexOf(
          "my-card bg-purple text-white"
        );
        if (index > -1) {
          this.categoryCardColor.splice(index, 1);
        }
        this.memberColor.unshift("purple");
        this.deletedColors.push("purple");
      } else if (color === "red") {
        const index = this.categoryCardColor.indexOf(
          "my-card bg-red text-white"
        );
        if (index > -1) {
          this.categoryCardColor.splice(index, 1);
        }
        this.memberColor.unshift("red");
        this.deletedColors.push("red");
      } else {
        const index = this.categoryCardColor.indexOf(
          "my-card bg-yellow text-white"
        );
        if (index > -1) {
          this.categoryCardColor.splice(index, 1);
        }
        this.memberColor.unshift("yellow");
        this.deletedColors.push("yellow");
      }
      var url =
        "http://46.18.25.97:8050/users/companion/delete/" +
        this.deletingId.toString();
      axios.delete(url).then(() => {
        var userToDelete = this.membersConnection[this.deletingId.toString()];
        delete this.memberPreference[this.deletingId];
        this.addedMember = this.addedMember.splice(userToDelete, 1);
        delete this.groupMembers[this.deletingId];
        var deletingIndicies = [];
        for (const [ind, element] of this.userPreferenceList.entries()) {
          if (element[1] === this.deletingId) {
            if (ind > -1) {
              deletingIndicies.push(ind);
            }
          }
        }
        deletingIndicies = deletingIndicies.reverse();
        for (var items of deletingIndicies) {
          this.userPreferenceList.splice(items, 1);
        }
        // this.userPreferenceList.push(tempList);
        this.qualityValidity = false;
        this.sizeValidity = false;
        this.getMenu();
        this.$emit("userPreferenceList", this.userPreferenceList);
        sessionStorage.setItem(
          "userPreferenceList",
          JSON.stringify(this.userPreferenceList)
        );
      });
      this.deleteDialog = false;
      // this.$q.notify({
      //   message: "Member is deleted.",
      //   icon: "person",
      //   color: "red",
      // });
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
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Select city " + String(city),
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
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
      var interactionData = {
        group_id: this.group_id_intract,
        interaction: "Set location",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
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
      var usrId = 0;
      for (var [key, value] of Object.entries(this.groupInfo)) {
        if (value[0] === "organizer") {
          usrId = key;
        }
      }
      if (this.remember[user_id] !== undefined) {
        var remeberingInteractionUsage = {
          user_id: usrId,
          group_id: this.group_id_intract,
          rembering_id: user_id,
          avialble_before: this.current,
          user_available_before:
            this.restCategorySize[user_id][this.memberPreference[user_id][0]],
        };
        remeberingInteractionUsage[food] =
          Object.keys(this.remember[user_id]).splice(0, 2).includes(food) &&
          !this.memberPreference[user_id].includes(food);
      }

      if (this.cantradictExpansionObj[user_id] !== undefined) {
        var contradictionInteractionUsage = {
          user_id: parseInt(usrId),
          group_id: parseInt(this.group_id_intract),
          vconflict_id: parseInt(user_id),
          limiting_member:
            parseInt(user_id) ===
            parseInt(
              Object.keys(
                Object.fromEntries(
                  Object.entries(this.limitingmembers).sort(
                    ([, a], [, b]) => a - b
                  )
                )
              )[0]
            ),
          avialble_before: this.current,
          revision_number: this.revisionSize,
          user_available_before:
            this.restCategorySize[user_id][this.memberPreference[user_id][0]],
        };
        contradictionInteractionUsage[food] =
          Object.keys(this.cantradictExpansionObj[user_id])
            .splice(0, 2)
            .includes(food) && !this.memberPreference[user_id].includes(food);
      }
      sessionStorage.setItem("relevanceValidation", false);
      sessionStorage.setItem("attractivenessValidation", false);
      sessionStorage.setItem("SimilarityValidation", false);
      var interactionData = {
        group_id: this.group_id_intract,
        interaction:
          "Preference " +
          String(food) +
          " is added to " +
          "user " +
          String(user_id),
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
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
        .then((response) => {
          if (this.revisionTriggre === true) {
            const url =
              "http://46.18.25.97:8050/contradiction/expansion/" +
              JSON.parse(sessionStorage.getItem("group_id"));
            axios.get(url).then((response) => {
              if (typeof response.data !== "undefined") {
                this.cantradictExpansionObj = response.data;
              }
            });
          }
        });
      var tempArray = this.memberPreference[user_id];
      if (!this.memberPreference[user_id].includes(food)) {
        tempArray.push(food);
        var tempList = [food, user_id];
        this.userPreferenceList.push(tempList);
        this.$emit("userPreferenceList", this.userPreferenceList);
        sessionStorage.setItem(
          "userPreferenceList",
          JSON.stringify(this.userPreferenceList)
        );
        if (name === "Organizer") {
          var nickname = "your";
        } else {
          var nickname = name;
        }
        // this.$q.notify({
        //   message:
        //     this.food_name_change(food) +
        //     " is added to " +
        //     nickname +
        //     " preferences",
        //   icon: "person",
        //   color: "green",
        // });
      } else {
        const index = tempArray.indexOf(food);
        tempArray.splice(index, 1);
        for (var i = 0; i < this.userPreferenceList.length; i++) {
          if (
            this.userPreferenceList[i][0] == food &&
            this.userPreferenceList[i][1] == user_id
          ) {
            var indexPref = i;
          }
        }
        this.userPreferenceList.splice(indexPref, 1);
        this.$emit("userPreferenceList", this.userPreferenceList);
        sessionStorage.setItem(
          "userPreferenceList",
          JSON.stringify(this.userPreferenceList)
        );
        if (name === "Organizer") {
          var nickname = "your";
        } else {
          var nickname = name;
        }
        // this.$q.notify({
        //   message:
        //     this.food_name_change(food) +
        //     " is deleted from " +
        //     nickname +
        //     " preferences",
        //   icon: "person",
        //   color: "red",
        // });
      }
      this.memberPreference[user_id] = tempArray;
      this.qualityValidity = false;
      this.sizeValidity = false;
      this.getMenu();
      if (this.remember[user_id] !== undefined) {
        remeberingInteractionUsage["user_available_after"] =
          this.restCategorySize[user_id][this.memberPreference[user_id][0]];
        remeberingInteractionUsage["avialble_after"] = this.current;
        if (this.suggestionType === "minfo") {
          axios
            .post(
              "http://46.18.25.97:8050/interaction/remebring/usage/storage",
              remeberingInteractionUsage
            )
            .then();
        }
      }
      if (this.cantradictExpansionObj[user_id] !== undefined) {
        contradictionInteractionUsage["user_available_after"] =
          this.restCategorySize[user_id][this.memberPreference[user_id][0]];
        contradictionInteractionUsage["avialble_after"] = this.current;
        if (this.suggestionType === "mprefs") {
          axios
            .post(
              "http://46.18.25.97:8050/interaction/conflict/usage/storage",
              contradictionInteractionUsage
            )
            .then();
        }
      }
      var countPref = 0;
      for (var prop of Object.keys(this.memberPreference)) {
        countPref =
          countPref + Object.values(this.memberPreference[prop]).length;
      }
      if (countPref > 0) {
        if (parseInt(sessionStorage.getItem("sorting")) < 0) {
          sessionStorage.setItem("sorting", 4);
        }
      } else {
        sessionStorage.setItem("sorting", -1);
      }
    },
    getMenu() {
      var listOfPref = Object.values(this.memberPreference).flat(1);
      if (String(sessionStorage.getItem("menuValidity")) !== "true") {
        var url = "http://46.18.25.97:8050/recommendations/popularity/";
        axios.get(url).then((response) => {
          var restaurantJson = JSON.parse(JSON.stringify(response.data));
          var counter = 2;
          this.restMenu = [];
          this.restMenuId = {};
          for (var restident of Object.values(restaurantJson)) {
            if (JSON.parse(restident).id !== undefined) {
              const urlmnue =
                "http://46.18.25.97:8050/restaurant/menu/id/" +
                JSON.parse(restident).id;
              axios.get(urlmnue).then((response) => {
                var menuListGet = JSON.parse(JSON.stringify(response.data));
                var restIdFor = menuListGet["id"];
                delete menuListGet.id;
                counter++;
                this.restMenu.push(menuListGet);
                this.restMenuId[restIdFor] = menuListGet;
                if (counter >= Object.keys(restaurantJson).length) {
                  sessionStorage.setItem(
                    "menuList",
                    JSON.stringify(this.restMenu)
                  );
                  sessionStorage.setItem(
                    "menuListId",
                    JSON.stringify(this.restMenuId)
                  );
                  this.qualityValidity = false;
                  this.sizeValidity = false;
                  this.getNewCategorySize();
                  this.getNewCategoryQualitySize();
                  sessionStorage.setItem("menuValidity", true);
                  this.menuValidity = true;
                }
              });
            }
          }
        });
      } else {
        this.restMenuId = JSON.parse(sessionStorage.getItem("menuListId"));
        this.restMenu = JSON.parse(sessionStorage.getItem("menuList"));
        this.qualityValidity = false;
        this.sizeValidity = false;
        this.getNewCategorySize();
        this.getNewCategoryQualitySize();
        this.menuValidity = true;
      }
    },
    getNewCategoryQualitySize() {
      this.qualityValidity = false;
      var listOfPref = Object.values(this.memberPreference).flat(1);
      for (var usr of Object.keys(this.memberPreference)) {
        var membersPrefs = this.memberPreference;
        var currentMemberPrefs = new Set(
          Object.values(this.memberPreference[usr])
        );
        var restCategorySizeEach = {};
        for (var food of this.foodsCategory) {
          let setList = [];
          for (var usrPrefs of Object.keys(membersPrefs)) {
            var tempy = new Set(Object.values(membersPrefs[usrPrefs]));
            if (usr !== usrPrefs) {
              if (tempy.size === 0) {
                tempy.add(food);
                setList.push(tempy);
              } else {
                setList.push(tempy);
              }
            } else {
              if (tempy.size === 0) {
                tempy.add(food);
                setList.push(tempy);
              } else {
                tempy.add(food);
                setList.push(tempy);
              }
            }
          }
          var categoryCounter = 0;
          var categoryCounterExisting = 0;
          var intersection = 0;
          for (var restIdLoop of Object.keys(this.restMenuId)) {
            var menu = this.restMenuId[restIdLoop];
            var selectedFoodFlagList = [];
            var existingCategory = new Set();
            existingCategory.clear();
            for (var x of Object.keys(menu)) {
              if (menu[x].length > 0) {
                existingCategory.add(x);
              }
            }
            for (var index in setList) {
              var menuIndividualList = [];
              menuIndividualList = [existingCategory, setList[index]];
              if (
                menuIndividualList.reduce(
                  (a, b) => new Set([...a].filter((x) => b.has(x)))
                ).size > 0
              ) {
                selectedFoodFlagList.push(true);
              } else {
                selectedFoodFlagList.push(false);
              }
            }

            if (
              selectedFoodFlagList.length === 0 ||
              (selectedFoodFlagList.every((v) => v === true) &&
                this.tripScore[restIdLoop] > 4)
            ) {
              categoryCounterExisting++;
            }
            if (
              selectedFoodFlagList.length === 0 ||
              selectedFoodFlagList.every((v) => v === true)
            ) {
              if (menu[food].length > 0) {
                intersection++;
              }
            }
          }

          restCategorySizeEach[food] = categoryCounterExisting;
        }
        this.restCategoryQualitySize[usr] = restCategorySizeEach;
        this.limitingmembersQualiry[usr] = Object.values(
          restCategorySizeEach
        ).reduce((a, b) => Math.max(a, b));
      }
      this.currentlyAvailableQuality();
      this.qualityValidity = true;
    },
    getNewCategorySize() {
      this.sizeValidity = false;
      var listOfPref = Object.values(this.memberPreference).flat(1);
      for (var usr of Object.keys(this.memberPreference)) {
        var membersPrefs = this.memberPreference;
        var currentMemberPrefs = new Set(
          Object.values(this.memberPreference[usr])
        );
        var restCategorySizeEach = {};
        for (var food of this.foodsCategory) {
          let setList = [];
          for (var usrPrefs of Object.keys(membersPrefs)) {
            var tempy = new Set(Object.values(membersPrefs[usrPrefs]));
            if (usr !== usrPrefs) {
              if (tempy.size === 0) {
                tempy.add(food);
                // setList.push(tempy);
              } else {
                setList.push(tempy);
              }
            } else {
              if (tempy.size === 0) {
                tempy.add(food);
                // setList.push(tempy);
              } else {
                tempy.add(food);
                setList.push(tempy);
              }
            }
          }
          var categoryCounter = 0;
          var categoryCounterExisting = 0;
          var intersection = 0;
          for (var menu of Object.values(this.restMenuId)) {
            var selectedFoodFlagList = [];
            var existingCategory = new Set();
            existingCategory.clear();
            for (var x of Object.keys(menu)) {
              if (menu[x].length > 0) {
                existingCategory.add(x);
              }
            }
            for (var index in setList) {
              var menuIndividualList = [];
              menuIndividualList = [existingCategory, setList[index]];
              if (setList[index].size > 0) {
                if (
                  menuIndividualList.reduce(
                    (a, b) => new Set([...a].filter((x) => b.has(x)))
                  ).size > 0
                ) {
                  selectedFoodFlagList.push(true);
                } else {
                  selectedFoodFlagList.push(false);
                }
              } else {
                continue;
              }
            }
            if (
              selectedFoodFlagList.length === 0 ||
              selectedFoodFlagList.every((v) => v === true)
            ) {
              categoryCounterExisting++;
            }
            if (
              selectedFoodFlagList.length === 0 ||
              selectedFoodFlagList.every((v) => v === true)
            ) {
              if (menu[food].length > 0) {
                intersection++;
              }
            }
          }
          if (this.memberPreference[usr].length > 0) {
            restCategorySizeEach[food] = categoryCounterExisting;
          } else {
            restCategorySizeEach[food] = intersection;
          }
        }
        this.restCategorySize[usr] = restCategorySizeEach;
        this.limitingmembers[usr] = Object.values(restCategorySizeEach).reduce(
          (a, b) => Math.max(a, b)
        );
      }
      this.currentlyAvailable();
      this.sizeValidity = true;
    },
    getUserAvilability(prefs) {
      var numberOfRestaurants = 0;
      let set1 = new Set(prefs);
      for (var index of Object.keys(this.restMenuId)) {
        var restMenuExist = [];
        for (var listOfMenu of Object.keys(this.restMenuId[index])) {
          if (this.restMenuId[index][listOfMenu].length > 0) {
            restMenuExist.push(listOfMenu);
          }
        }
        let set2 = new Set(restMenuExist);
        let set = new Set([...set1].filter((x) => set2.has(x)));
        if (set.size > 0) {
          numberOfRestaurants++;
        }
      }

      return numberOfRestaurants;
    },
    getUserAvilabilityQuality(prefs) {
      var numberOfRestaurants = 0;
      let set1 = new Set(prefs);
      for (var index of Object.keys(this.restMenuId)) {
        if (this.tripScore[index] > 4) {
          var restMenuExist = [];
          for (var listOfMenu of Object.keys(this.restMenuId[index])) {
            if (this.restMenuId[index][listOfMenu].length > 0) {
              restMenuExist.push(listOfMenu);
            }
          }
          let set2 = new Set(restMenuExist);
          let set = new Set([...set1].filter((x) => set2.has(x)));
          if (set.size > 0) {
            numberOfRestaurants++;
          }
        }
      }
      return numberOfRestaurants;
    },
    currentlyAvailable() {
      var listOfPref = Object.values(this.memberPreference).flat(1);

      for (var usr of Object.keys(this.memberPreference)) {
        var membersPrefs = this.memberPreference;
        if (this.memberPreference[usr] > 0) {
          var currentMemberPrefs = new Set(
            Object.values(this.memberPreference[usr])
          );
        } else {
          var currentMemberPrefs = new Set(this.foodsCategory);
        }
        var restCategorySizeEach = {};
        for (var food of this.foodsCategory) {
          let setList = [];
          for (var usrPrefs of Object.keys(membersPrefs)) {
            if (Object.values(membersPrefs[usrPrefs]).length > 0) {
              var tempy = new Set(Object.values(membersPrefs[usrPrefs]));
              if (usr !== usrPrefs) {
                if (tempy.size === 0) {
                  setList.push(tempy);
                } else {
                  setList.push(tempy);
                }
              } else {
                if (tempy.size === 0) {
                  setList.push(tempy);
                } else {
                  setList.push(tempy);
                }
              }
            }
          }
          var categoryCounter = 0;
          var categoryCounterExisting = 0;
          var intersection = 0;
          for (var menu of Object.values(this.restMenuId)) {
            var selectedFoodFlagList = [];
            var existingCategory = new Set();
            existingCategory.clear();
            for (var x of Object.keys(menu)) {
              if (menu[x].length > 0) {
                existingCategory.add(x);
              }
            }
            for (var index in setList) {
              var menuIndividualList = [];
              menuIndividualList = [existingCategory, setList[index]];
              if (
                menuIndividualList.reduce(
                  (a, b) => new Set([...a].filter((x) => b.has(x)))
                ).size > 0
              ) {
                selectedFoodFlagList.push(true);
              } else {
                selectedFoodFlagList.push(false);
              }
            }

            if (
              selectedFoodFlagList.length === 0 ||
              selectedFoodFlagList.every((v) => v === true)
            ) {
              categoryCounterExisting++;
            }
          }
          restCategorySizeEach[food] = categoryCounterExisting;
        }

        this.current = categoryCounterExisting;
        this.$emit("currentRestaurants", this.current);
      }
    },
    currentlyAvailableQuality() {
      var listOfPref = Object.values(this.memberPreference).flat(1);

      for (var usr of Object.keys(this.memberPreference)) {
        var membersPrefs = this.memberPreference;
        if (this.memberPreference[usr] > 0) {
          var currentMemberPrefs = new Set(
            Object.values(this.memberPreference[usr])
          );
        } else {
          var currentMemberPrefs = new Set(this.foodsCategory);
        }
        var restCategorySizeEach = {};
        for (var food of this.foodsCategory) {
          let setList = [];
          for (var usrPrefs of Object.keys(membersPrefs)) {
            if (Object.values(membersPrefs[usrPrefs]).length > 0) {
              var tempy = new Set(Object.values(membersPrefs[usrPrefs]));
              if (usr !== usrPrefs) {
                if (tempy.size === 0) {
                  setList.push(tempy);
                } else {
                  setList.push(tempy);
                }
              } else {
                if (tempy.size === 0) {
                  setList.push(tempy);
                } else {
                  setList.push(tempy);
                }
              }
            }
          }
          var categoryCounter = 0;
          var categoryCounterExisting = 0;
          var intersection = 0;
          for (var restIdLoop of Object.keys(this.restMenuId)) {
            var menu = this.restMenuId[restIdLoop];
            var selectedFoodFlagList = [];
            var existingCategory = new Set();
            existingCategory.clear();
            for (var x of Object.keys(menu)) {
              if (menu[x].length > 0) {
                existingCategory.add(x);
              }
            }
            for (var index in setList) {
              var menuIndividualList = [];
              menuIndividualList = [existingCategory, setList[index]];
              if (
                menuIndividualList.reduce(
                  (a, b) => new Set([...a].filter((x) => b.has(x)))
                ).size > 0
              ) {
                selectedFoodFlagList.push(true);
              } else {
                selectedFoodFlagList.push(false);
              }
            }

            if (
              selectedFoodFlagList.length === 0 ||
              (selectedFoodFlagList.every((v) => v === true) &&
                this.tripScore[restIdLoop] > 4)
            ) {
              categoryCounterExisting++;
            }
          }

          restCategorySizeEach[food] = categoryCounterExisting;
        }
        this.highQuality = categoryCounterExisting;
      }
    },
    // test() {
    //   var listOfPref = Object.values(this.memberPreference).flat(1);
    //   let setList = [];
    //   for (var usrPrefs of Object.values(this.memberPreference)) {
    //     setList.push(new Set(Object.values(usrPrefs)));
    //   }
    //   for (var usr of Object.keys(this.memberPreference)) {
    //     var restCategorySizeEach = {};
    //     for (var food of this.foodsCategory) {
    //       var categoryCounter = 0;
    //       for (var menu of this.restMenu) {
    //         var selectedFoodFlagList = [];
    //         var existingCategory = new Set();
    //         for (var x of Object.keys(menu)) {
    //           if (menu[x].length > 0) {
    //             existingCategory.add(x);
    //           }
    //         }
    //         for (var index in setList) {
    //           var menuIndividualList = [];
    //           menuIndividualList = [existingCategory, setList[index]];
    //           if ((setList.length = 0)) {
    //             selectedFoodFlagList.push(true);
    //           } else if (
    //             setList.length > 0 &&
    //             menuIndividualList.reduce(
    //               (a, b) => new Set([...a].filter((x) => b.has(x)))
    //             ).size > 0
    //           ) {
    //             selectedFoodFlagList.push(true);
    //           } else {
    //             selectedFoodFlagList.push(false);
    //           }
    //         }
    //         if (
    //           menu[food].length > 0 &&
    //           (selectedFoodFlagList.length === 0 ||
    //             selectedFoodFlagList.every((v) => v === true))
    //         ) {
    //           categoryCounter++;
    //         }
    //       }
    //       restCategorySizeEach[food] = categoryCounter;
    //     }
    //     this.restCategorySize[usr] = restCategorySizeEach;
    //   }
    // },
    // testQuality() {
    //   var listOfPref = Object.values(this.memberPreference).flat(1);
    //   let setList = [];
    //   for (var usrPrefs of Object.values(this.memberPreference)) {
    //     setList.push(new Set(Object.values(usrPrefs)));
    //   }
    //   for (var usr of Object.keys(this.memberPreference)) {
    //     var restCategorySizeEach = {};
    //     for (var food of this.foodsCategory) {
    //       var categoryCounter = 0;
    //       for (var restIdLoop of Object.keys(this.restMenuId)) {
    //         var menu = this.restMenuId[restIdLoop];
    //         var selectedFoodFlagList = [];
    //         var existingCategory = new Set();
    //         for (var x of Object.keys(menu)) {
    //           if (menu[x].length > 0) {
    //             existingCategory.add(x);
    //           }
    //         }
    //         for (var index in setList) {
    //           var menuIndividualList = [];
    //           menuIndividualList = [existingCategory, setList[index]];
    //           if ((setList.length = 0)) {
    //             selectedFoodFlagList.push(true);
    //           } else if (
    //             setList.length > 0 &&
    //             menuIndividualList.reduce(
    //               (a, b) => new Set([...a].filter((x) => b.has(x)))
    //             ).size > 0
    //           ) {
    //             selectedFoodFlagList.push(true);
    //           } else {
    //             selectedFoodFlagList.push(false);
    //           }
    //         }
    //         if (
    //           menu[food].length > 0 &&
    //           (selectedFoodFlagList.length === 0 ||
    //             selectedFoodFlagList.every((v) => v === true)) &&
    //           this.tripScore[parseInt(restIdLoop)] > 4
    //         ) {
    //           categoryCounter++;
    //         }
    //       }
    //       restCategorySizeEach[food] = categoryCounter;
    //     }
    //     this.restCategoryQualitySize[usr] = restCategorySizeEach;
    //   }
    // },
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

    getContradiction(recievedId) {
      var usrId = 0;
      for (var [key, value] of Object.entries(this.groupInfo)) {
        if (value[0] === "organizer") {
          usrId = key;
        }
      }
      var contradictionInteraction = {
        user_id: usrId,
        group_id: this.group_id_intract,
        user_to_add_id: recievedId,
      };
      axios
        .post(
          "http://46.18.25.97:8050/interaction/conflict/storage",
          contradictionInteraction
        )
        .then();
      this.$q.loading.show();
      const url =
        "http://46.18.25.97:8050/contradiction/expansion/" +
        JSON.parse(sessionStorage.getItem("group_id"));
      axios.get(url).then((response) => {
        if (typeof response.data !== "undefined") {
          this.cantradictExpansionObj = response.data;
          this.$q.loading.hide();
        }
        this.expandCotradiction = true;
      });
    },
  },
  mounted() {
    if (JSON.parse(sessionStorage.getItem("rememberInfo")) !== null) {
      this.remember = JSON.parse(sessionStorage.getItem("rememberInfo"));
    }
    if (this.revisionTriggre === true) {
      this.suggestionType = "mprefs";
      const url =
        "http://46.18.25.97:8050/contradiction/expansion/" +
        JSON.parse(sessionStorage.getItem("group_id"));
      axios.get(url).then((response) => {
        if (typeof response.data !== "undefined") {
          this.cantradictExpansionObj = response.data;
          this.expandCotradiction = true;
        }
      });
    }
    this.scrollToTop();
    if (JSON.parse(sessionStorage.getItem("userPreferenceList")) !== null) {
      this.userPreferenceList = [];
      this.userPreferenceList = JSON.parse(
        sessionStorage.getItem("userPreferenceList")
      );
    } else {
      this.userPreferenceList = [];
    }
    for (var user in this.groupInfo) {
      this.memberCounter--;
      this.editableVisibility.push(true);
      var rmIndex = this.memberColor.indexOf(this.groupInfo[user][0]);
      if (rmIndex > -1) {
        this.memberColor.splice(rmIndex, 1);
        if (this.groupInfo[user][0] === "orange") {
          this.categoryCardColor.push("my-card bg-orange text-white");
        } else if (this.groupInfo[user][0] === "purple") {
          this.categoryCardColor.push("my-card bg-purple text-white");
        } else if (this.groupInfo[user][0] === "red") {
          this.categoryCardColor.push("my-card bg-red text-white");
        } else {
          this.categoryCardColor.push("my-card bg-yellow text-white");
        }
      }
    }
    this.memberCounter++;
    if (String(sessionStorage.getItem("Selected")) === "true") {
      this.endOfSession = true;
    } else {
      this.endOfSession = false;
    }
    if (JSON.parse(sessionStorage.getItem("group_id")) !== null) {
      const url =
        "http://46.18.25.97:8050/preferences/" +
        JSON.parse(sessionStorage.getItem("group_id"));
      axios.get(url).then((response) => {
        if (typeof response.data !== "undefined") {
          this.memberPreference = response.data;
          if (Object.keys(this.organizerId).length === 0) {
            this.getMenu();
          }
        }
      });
    }
    this.foodCategoryObjName = Object.keys(this.foodCategoryObj);
    this.foodCategoryObjNameDefault = Object.keys(this.foodCategoryObjDefault);
    this.options = this.foodCategoryObjName;
    //   VueGeolocation.getLocation().then(coordinates => {
    // });
    if (Object.keys(this.organizerId).length > 0) {
      this.$emit("groupConstructed");
      var memberId = Object.keys(this.organizerId)[0];
      const url = "http://46.18.25.97:8050/user/get/group/" + String(memberId);
      axios.get(url).then((response) => {
        this.membersInfo = response.data;
        if (
          typeof this.membersInfo === "object" &&
          Object.keys(this.membersInfo).length > 0
        ) {
          var progressUpdate = {
            user_id: memberId,
            column_name: "group_construction",
            group_construction: true,
          };
          axios
            .post(
              "http://46.18.25.97:8050/user/update/progress",
              progressUpdate
            )
            .then((response) => {});
          var registerationId = -1;
          const url2 =
            "http://46.18.25.97:8050/get/registeration/id/" + String(memberId);
          var supports = {
            user_id: 0,
            info_level: 3,
            expansion: 0,
            contradiction: 0,
          };
          axios.get(url2).then((response) => {
            var returnedId = response.data;
            supports["user_id"] = memberId;
            if (this.stepSend < 3 && returnedId % 3 === 1) {
              for (var uuId of Object.keys(this.membersInfo)) {
                this.membersInfo[uuId]["preference"] = [];
                supports["info_level"] = 2;
              }
            }
            if (this.stepSend < 3 && returnedId % 3 === 2) {
              for (var uuId of Object.keys(this.membersInfo)) {
                this.membersInfo[uuId]["preference"] = [];
                this.membersInfo[uuId]["cuisine"] = [];
                supports["info_level"] = 1;
              }
            }
            var secondDigit = parseInt(
              String(returnedId).charAt(String(returnedId).length - 1)
            );
            if (
              JSON.parse(sessionStorage.getItem("preferenceExpansion")) === null
            ) {
              if (secondDigit < 10) {
                this.preferenceExpansion = true;
                supports["expansion"] = 1;
                sessionStorage.setItem("preferenceExpansion", true);
              } else {
                this.preferenceExpansion = false;
                supports["expansion"] = 0;
                sessionStorage.setItem("preferenceExpansion", false);
              }
            } else {
              this.preferenceExpansion = JSON.parse(
                sessionStorage.getItem("preferenceExpansion")
              );
              supports["expansion"] = JSON.parse(
                sessionStorage.getItem("preferenceExpansion")
              );
            }
            if (
              JSON.parse(sessionStorage.getItem("preferenceContradiction")) ===
              null
            ) {
              if (-1 < secondDigit && secondDigit < 10) {
                this.preferenceContradiction = true;
                supports["contradiction"] = 1;
                sessionStorage.setItem("preferenceContradiction", true);
              } else {
                this.preferenceContradiction = false;
                supports["contradiction"] = 0;
                sessionStorage.setItem("preferenceContradiction", false);
              }
            } else {
              this.preferenceContradiction = JSON.parse(
                sessionStorage.getItem("preferenceContradiction")
              );
              supports["contradiction"] = JSON.parse(
                sessionStorage.getItem("preferenceContradiction")
              );
            }
            axios
              .post("http://46.18.25.97:8050/set/user/support/", supports)
              .then((response) => {});
          });
        }
        if (
          JSON.parse(sessionStorage.getItem("initialPreferenceSet")) !== true &&
          JSON.parse(sessionStorage.getItem("group_id")) !== null
        ) {
          const url =
            "http://46.18.25.97:8050/preferences/" +
            JSON.parse(sessionStorage.getItem("group_id"));
          axios.get(url).then((response) => {
            if (typeof response.data !== "undefined") {
              this.memberPreference = response.data;

              for (var userIds of Object.keys(this.memberPreference)) {
                for (var usrPrefsDelete of response.data[userIds]) {
                  this.addPreferences(userIds, usrPrefsDelete, "-1");
                }
                this.memberPreference[userIds] = [];
                sessionStorage.setItem("initialPreferenceSet", true);
              }
              if (Object.keys(this.organizerId).length > 0) {
                this.getMenu();
              }
            }
          });
        } else {
          this.getMenu();
        }

        // this.memberPreference = {};
        // this.memberPreference[memberId] = [];
        // this.getMenu();
      });
    }
  },
};
</script>

<style scoped>
/* .footer {
  position: fixed;
  bottom: 0;
  width: 100%;
} */
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
  padding-bottom: 10px;
  margin: 10px;
}
.groupInfoText {
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
</style>
