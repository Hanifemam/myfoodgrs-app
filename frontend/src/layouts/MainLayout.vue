<template>
  <div
    v-if="this.pageLoad"
    style="
      max-width: 600px;
      max-height: 100%;
      width: 100%;
      display: block;
      margin-left: auto;
      margin-right: auto;
    "
  >
    <!-- <q-dialog v-model="confirm" persistent>
      <q-card>
        <q-card-section class="row items-center" align="left">
          <span class="q-ml-sm">
            <p
              style="
                text-align: justify;
                padding-top: 10px;
                padding-left: 10px;
                padding-right: 10px;
              "
            >
              To use our application, you first need to add your group members
              and their preferences using the <strong>GROUP</strong> page in the
              application. Then, you can check the recommendations for your
              group on the <strong> RESTAURANT </strong>page. In the RESTAURANT
              page by clicking on the each restaurant card, you can find
              provided information about the suitability of the restaurant for
              your group and a specific member of your group. You can bookmark
              interesting restaurants. The bookmarked restaurants are available
              on the <strong>BOOKMARK</strong> page where you can compare the
              bookmarked restaurants and select one them as the final choice.
            </p>
          </span>
        </q-card-section>

        <q-card-actions align="left">
          <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog> -->
    <!-- <div v-if="frontPage" class="front">
      <q-layout view="lHh Lpr lFf">
         <div class="parent">
        <img
          src="../assets/myfoodheader.png"
          style="height: 60px; padding: 10px; border-radius: 5px"
        />
      </div>
      <div class="q-pa-md row items-start q-gutter-md" style="margin: auto">
        <q-card
          class="my-card individual"
          style="width: 95%; height: 200px; margin: 30px auto"
          @click="goIndividual()"
        >
          <q-card-section style="padding: px">
            <p class="textblack">INDIVIDUAL RECOMMENDATIONS?</p>
            <p class="textblack">CLICK HERE</p>
          </q-card-section>
        </q-card>
      </div> -->
    <!-- <div class="q-pa-md row items-start q-gutter-md" style="margin: auto">
          <q-card
            class="my-card group"
            style="width: 95%; height: 200px; margin: 30px auto"
            @click="goGroup()"
          >
            <q-card-section style="padding: 5px">
              <q-card-section style="padding: px">
                <p class="textwhite">GROUP RECOMMENDATIONS?</p>
                <p class="textwhite">CLICK HERE</p>
              </q-card-section>
            </q-card-section>
          </q-card>
        </div>
        <div
          class="q-pa-md row items-start q-gutter-md parent"
          style="margin: auto"
        >
          <q-card
            class="my-card"
            style="width: 95%; margin: 0px auto; opacity: 0.9"
          >
            <q-card-section style="padding: 10px; text-align: justify">
              Thanks for participating in this user study. Imagine you are the
              organizer of a dinner event, and you want to invite a group of
              friends or colleagues for dinner at a restaurant. This application
              aims to help you in finding a proper restaurant for a group of
              people. In this application, you can introduce new group members,
              add their preferences, use different recommendation methods and
              visual explanations, browse the restaurant page, bookmark them,
              compare them on the bookmark page, and finally select one of the
              bookmarked items as the final choice. In the end, the system asks
              a few questions about your experience with the system. There is
              also a text area on this last page where you can add your
              comments, ideas, and critiques about the system.
            </q-card-section>
          </q-card>
        </div>
      </q-layout> -->
    <!-- </div> -->
    <div
      v-if="individual"
      class="scroll"
      style="
        max-width: 30%;
        display: block;
        margin-left: auto;
        margin-right: auto;
      "
    >
      <q-layout view="lHh Lpr lFf">
        <q-header
          elevated
          style="
            max-width: 30%;
            display: block;
            margin-left: auto;
            margin-right: auto;
          "
        >
          <q-toolbar>
            <q-btn
              flat
              dense
              round
              icon="menu"
              aria-label="Menu"
              @click="toggleLeftDrawer"
            />

            <q-toolbar-title>
              <p style="align: right">MyFood</p>
              <p style="align: left">MyFood</p>
            </q-toolbar-title>
          </q-toolbar>
        </q-header>
        <!-- Uncomment for next step -->
        <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
          <q-list>
            <q-item-label header> Essential Links </q-item-label>
          </q-list>
        </q-drawer>
        <!-- Uncomment for next step -->
        <q-footer
          style="
            max-width: 30%;
            display: block;
            margin-left: auto;
            margin-right: auto;
          "
        >
          <q-layout
            view="lHh lpr lFf"
            container
            style="height: 45px"
            class="shadow-2 rounded-borders"
          >
            <q-header elevated>
              <q-tabs v-model="tab" inline-label active-bg-color="indigo-3">
                <q-tab
                  class="size"
                  name="Group"
                  label="Group"
                  icon="group"
                  style="padding: 3px"
                  @click="determinePageInd('user')"
                />
                <q-tab
                  class="size"
                  name="Restuarants"
                  label="Restuarant"
                  icon="restaurant"
                  style="padding: 3px"
                  @click="determinePageInd('urest')"
                />
                <q-tab
                  class="size"
                  name="Bookmark"
                  label="Bookmark"
                  icon="favorite"
                  style="padding: 3px"
                  @click="determinePageInd('ubook')"
                />
              </q-tabs>
            </q-header>
          </q-layout>
        </q-footer>
        <!-- <q-layout
      view="lHh lpr lFf"
      container
      style="height: 120px"
      class="shadow-2 rounded-borders"
    >
      <q-header elevated>
        <q-toolbar>


          <q-toolbar-title> MyFoodInd </q-toolbar-title>
        </q-toolbar>
        <q-tabs no-caps active-color="primary" class="text-grey" v-model="tab">
          <q-tab
            name="Preferences"
            label="Preferences"
            icon="person"
            @click="determinePageInd('user')"
          />
          <q-tab
            name="Restuarants"
            label="Restuarants"
            icon="restaurant"
            @click="determinePageInd('urest')"
          />
          <q-tab
            name="Bookmark"
            label="Bookmark"
            icon="favorite"
            @click="determinePageInd('ubook')"
          />
        </q-tabs>
      </q-header> -->

        <!-- <q-drawer v-model="leftDrawerOpen" show-if-above bordered>
      <q-list>
        <q-item-label header> Essential Links </q-item-label>

        <EssentialLink
          v-for="link in essentialLinks"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer> -->
        <!-- <q-footer bordered class="bg-white text-primary"> </q-footer>
      <q-footer reveal elevated> </q-footer> -->
        <UserPage v-if="pageInd === 'user'" :groupInfo="groupInfo"></UserPage>
        <UserRestaurantpage
          v-if="pageInd === 'urest' && propsGroupID > 0"
          :groupInfo="groupInfo"
          :groupId="propsGroupID"
        ></UserRestaurantpage>
        <UserBookmarkpage
          v-if="pageInd === 'ubook' && propsGroupID > 0"
          :groupInfo="groupInfo"
          :groupId="propsGroupID"
          @critique-issued="emitedCritique()"
        ></UserBookmarkpage>
      </q-layout>
    </div>
    <div v-if="group" class="scroll" style="width: 100%">
      <q-layout view="lHh Lpr lFf" style="min-height: 100%">
        <q-header
          elevated
          style="
            max-width: 600px;
            width: 100%;
            display: block;
            margin-left: auto;
            margin-right: auto;
          "
        >
          <q-toolbar>
            <!-- Uncomment for next step -->
            <q-btn
              flat
              dense
              round
              icon="menu"
              aria-label="Menu"
              @click="toggleLeftDrawer"
            />
            <!-- Uncomment for next step -->

            <q-toolbar-title style="padding-left: 2px; vertical-align: middle">
              <div style="display: flex; height: auto; margin-bottom: 0px">
                <p
                  style="
                    height: 100%;
                    text-align: left;
                    width: 50%;
                    font-size: large;
                    margin-bottom: 0px;
                    vertical-align: middle;
                  "
                >
                  MyFood
                </p>
                <!-- Uncomment for next step -->
                <p
                  style="
                    text-align: right;
                    width: 50%;
                    font-size: small;
                    margin-bottom: 0px;
                    vertical-align: top;
                    padding-top: 4px;
                  "
                >
                  ✋ Hi {{ userName }}
                </p>
                <!-- Uncomment for next step -->
              </div>
            </q-toolbar-title>
          </q-toolbar>
        </q-header>
        <!-- Uncomment for next step -->
        <q-drawer
          v-model="leftDrawerOpen"
          show-if-above
          bordered
          :width="$q.screen.width"
        >
          <q-list>
            <q-item-label header>
              <q-icon name="arrow_back" @click="drawerToggle()" size="1.3rem" />
            </q-item-label>

            <EssentialLink
              @nameDedicated="namededicated"
              @userIdDictated="userIdDictated"
              @stepEmit="stepEmit"
              :itemSelected="itemSelected"
              :groupConstructedValidator="groupConstructedValidator"
            />
          </q-list>
        </q-drawer>
        <!-- Uncomment for next step -->

        <q-footer
          style="
            max-width: 600px;
            width: 100%;
            display: block;
            margin-left: auto;
            margin-right: auto;
          "
        >
          <q-layout
            view="lHh lpr lFf"
            container
            style="height: 45px"
            class="shadow-2 rounded-borders"
          >
            <q-header elevated>
              <q-tabs
                v-model="tab"
                inline-label
                active-color="indigo-3"
                align="justify"
                narrow-indicator
              >
                <q-tab
                  class="size"
                  name="Group"
                  label="Group"
                  icon="group"
                  style="padding: 3px"
                  @click="determinePage('group')"
                />
                <q-tab
                  class="size"
                  name="Restuarants"
                  label="Restuarant"
                  icon="restaurant"
                  style="padding: 3px"
                  @click="determinePage('rest')"
                />
                <q-tab
                  class="size"
                  name="Bookmark"
                  label="Bookmark"
                  icon="favorite"
                  style="padding: 3px"
                  @click="determinePage('book')"
                />
              </q-tabs>
            </q-header>
          </q-layout>
        </q-footer>
        <GroupPage
          v-if="page === 'group'"
          :groupInfo="groupInfo"
          :organizerId="organizerId"
          :critiqueRange="critiqueRange"
          :revisionTriggre="revisionTriggre"
          :stepSend="stepSend"
          :revisionSizeRecieved="revisionSizeRecieved"
          @groupConstructed="groupConstructed()"
          @currentRestaurants="currentRestaurants($event)"
          @userPreferenceList="trasmistUserPreferenceList($event)"
          @critique-issued="emitedCritique($event)"
        ></GroupPage>
        <RestaurantPage
          v-if="page === 'rest' && propsGroupID > 0"
          :currentRestaurant="currentRestaurant"
          :groupInfo="groupInfo"
          :groupId="propsGroupID"
          :critiqueRange="critiqueRange"
          :userPreferenceList="userPreferenceListTransfer"
          :revisionSizeRecieved="revisionSizeRecieved"
          @critique-issued="emitedCritique($event)"
          @goToGroupPage="goToGroupPage($event)"
          @activeRevision="activeRevision($event)"
        ></RestaurantPage>
        <BookmarkPage
          v-if="page === 'book' && propsGroupID > 0"
          :groupInfo="groupInfo"
          :groupId="propsGroupID"
          :organizerId="organizerId"
          :critiqueRange="critiqueRange"
          :userPreferenceList="userPreferenceListTransfer"
          @critique-issued="emitedCritique($event)"
          @RestSelected="RestSelected()"
          @goToGroupPage="goToGroupPage($event)"
          @activeRevision="activeRevision($event)"
        ></BookmarkPage>
      </q-layout>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref } from "vue";
// Uncomment for next step
import EssentialLink from "components/EssentialLink.vue";
import GroupPage from "components/GroupPage.vue";
import BookmarkPage from "components/BookmarkPage.vue";
import RestaurantPage from "components/RestaurantPage.vue";
import UserPage from "components/UserPage.vue";
import UserBookmarkpage from "components/UserBookmarkPage.vue";
import UserRestaurantpage from "components/UserRestaurantPage.vue";
import axios from "axios";
import VueGoogleMaps from "@fawmi/vue-google-maps";

const linksList = [
  {
    title: "Twitter",
    caption: "@quasarframework",
    icon: "rss_feed",
    link: "https://twitter.quasar.dev",
  },
  {
    title: "Facebook",
    caption: "@QuasarFramework",
    icon: "public",
    link: "https://facebook.quasar.dev",
  },
  {
    title: "Quasar Awesome",
    caption: "Community Quasar projects",
    icon: "favorite",
    link: "https://awesome.quasar.dev",
  },
];

export default {
  name: "MainLayout",
  components: {
    EssentialLink,
    GroupPage,
    RestaurantPage,
    BookmarkPage,
    UserPage,
    UserBookmarkpage,
    UserRestaurantpage,
  },

  setup() {
    const leftDrawerOpen = ref(false);

    return {
      propsGroupID: -1,

      // essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        var interactionData = {
          group_id: parseInt(sessionStorage.getItem("group_id")),
          interaction: "toggleLeftDrawer",
        };
        axios
          .post("http://46.18.25.97:8050/interaction", interactionData)
          .then();
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
  data() {
    return {
      currentRestaurant: 0,
      pageLoad: false,
      stepSend: 1,
      usrToDelete: -1,
      confirm: "",
      tab: ref("Restuarants"),
      individual: false,
      group: true,
      frontPage: false,
      page: "group",
      pageInd: "rest",
      groupInfo: {},
      membersName: {},
      default_member_info: {},
      userInfo: 0,
      userName: "Guest",
      organizerId: -1,
      itemSelected: false,
      groupConstructedValidator: false,
      userPreferenceListTransfer: [],
      critiqueRange: "",
      revisionTriggre: false,
      revisionSizeRecieved: 5,
    };
  },
  methods: {
    currentRestaurants(current) {
      this.currentRestaurant = current;
    },
    stepEmit() {
      this.stepSend = 3;
    },
    activeRevision(index) {
      this.revisionTriggre = true;
      this.revisionSizeRecieved = index + 1;
    },
    goToGroupPage(revision) {
      if (revision === true) {
        this.revisionTriggre = true;
      } else {
        this.revisionTriggre = false;
      }
      this.page = "group";
      this.frontPage = false;
      this.group = true;
      this.tab = ref("Group");
    },
    trasmistUserPreferenceList(userPreferenceList) {
      this.userPreferenceListTransfer = userPreferenceList;
    },
    groupConstructed() {
      this.groupConstructedValidator = true;
    },
    RestSelected() {
      this.itemSelected = true;
    },
    drawerToggle() {
      this.leftDrawerOpen = !this.leftDrawerOpen;
    },
    goIndividual() {
      this.frontPage = false;
      this.individual = true;
    },
    goGroup() {
      this.frontPage = false;
      this.group = true;
    },
    emitedCritique(range) {
      this.tab = ref("Restuarants");
      this.critiqueRange = range;
      var interactionData = {
        group_id: parseInt(sessionStorage.getItem("group_id")),
        interaction: "Visit page rest",
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.page = "rest";
    },
    userIdDictated(userInfoRecieved) {
      if (this.userName !== "Guest" || this.userName !== "guest") {
        if (typeof userInfoRecieved !== undefined) {
          this.organizerId = userInfoRecieved;
          this.groupInfo = {};
          this.groupInfo[Object.keys(userInfoRecieved)[0]] = [
            "organizer",
            Object.values(userInfoRecieved)[0],
          ];
          this.userName = Object.values(userInfoRecieved)[0];
          var user_temp_object = {
            first_name: Object.values(userInfoRecieved)[0],
            last_name: "string",
            email: "string",
            latitude: 0,
            longitude: 0,
            role: "organizer",
            group_id: sessionStorage.getItem("group_id"),
          };
          var url =
            "http://46.18.25.97:8050/users/update/organizer/groupid/" +
            Object.keys(userInfoRecieved)[0].toString();
          var request = "POST";
          var data = JSON.stringify(user_temp_object);
          this.sendRequestUpdate(
            url,
            request,
            data,
            "organizer",
            "update",
            Object.keys(userInfoRecieved)[0]
          );
        }
      } else {
        this.organizerId = {};
      }
      // For using the previous preferences just replace this.groupInfo with userInfoRecieved
    },
    namededicated(orgName) {
      this.userName = orgName;
    },
    determinePageInd(pageToChange) {
      var interactionData = {
        group_id: parseInt(sessionStorage.getItem("group_id")),
        interaction: "Visit page " + pageToChange,
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.pageInd = pageToChange;
    },
    determinePage(pageToChange) {
      var interactionData = {
        group_id: parseInt(sessionStorage.getItem("group_id")),
        interaction: "Visit page " + pageToChange,
      };
      axios.post("http://46.18.25.97:8050/interaction", interactionData).then();
      this.page = pageToChange;
    },
    sendRequestUpdate(url, request, data, role, type, userId) {
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
            if (response.status !== 200) {
              location.reload();
            }
            temp_user_id = JSON.parse(response.data);
            sessionStorage.setItem("userInfo", temp_user_id);
            sessionStorage.setItem(role, temp_user_id);
            sessionStorage.setItem(role_name, first_name);
            this.groupInfo = {};
            this.groupInfo[temp_user_id] = [role, first_name];
            var url =
              "http://46.18.25.97:8050/user/get/group/members/" +
              String(this.propsGroupID);
            axios.get(url).then((response) => {
              var groupMembers = response.data;
              for (var user of groupMembers) {
                if (!Object.keys(this.groupInfo).includes(String(user))) {
                  var url =
                    "http://46.18.25.97:8050/users/organizer/delete/" +
                    user.toString();
                  axios.delete(url).then((response) => {
                    var temp_element_to_add = {};
                    temp_element_to_add["id"] = temp_user_id;
                    temp_element_to_add["name"] = first_name;
                    temp_element_to_add["show"] = true;
                    this.membersName[role] = temp_element_to_add;
                    this.default_member_info = this.membersName;
                    return temp_user_id;
                  });
                }
              }
            });
          });
      }
    },
    sendRequest(url, request, data, role, type) {
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
            sessionStorage.setItem("userInfo", temp_user_id);
            sessionStorage.setItem(role, temp_user_id);
            sessionStorage.setItem(role_name, first_name);
            this.groupInfo[temp_user_id] = [role, first_name];
            var temp_element_to_add = {};
            temp_element_to_add["id"] = temp_user_id;
            temp_element_to_add["name"] = first_name;
            temp_element_to_add["show"] = true;
            this.membersName[role] = temp_element_to_add;
            this.default_member_info = this.membersName;
            this.usrToDelete = temp_user_id;
            return temp_user_id;
          });
      }
    },
    beforeWindowUnload(e) {
      e.preventDefault();
      e.returnValue = "";
    },
  },
  mounted() {
    sessionStorage.clear();
    sessionStorage.removeItem("sorting");
    sessionStorage.removeItem("initialPreferenceSet");
    sessionStorage.removeItem("group_id");
    sessionStorage.removeItem("location");
    sessionStorage.removeItem("group_members_status");
    sessionStorage.removeItem("Selected");
    sessionStorage.removeItem("menuListId");
    sessionStorage.removeItem("menuList");
    sessionStorage.clear();
    sessionStorage.setItem("menuValidity", false);
    sessionStorage.setItem("sorting", -1);
    sessionStorage.setItem("location", false);
    sessionStorage.setItem("sorting", -2);
    sessionStorage.setItem(
      "group_members_status",
      JSON.stringify({
        Blue: true,
        Green: true,
        Purple: true,
        Red: true,
        Yellow: true,
      })
    );
    var user = {
      first_name: "Organizer",
      last_name: "string",
      email: "string",
      latitude: 0,
      longitude: 0,
      role: "organizer",
      group_id: 0,
    };
    this.$q.loading.show();
    axios.get("http://46.18.25.97:8050/group").then((response) => {
      this.$q.loading.hide();
      this.pageLoad = true;
      this.propsGroupID = JSON.parse(response.data)["group_id"];
      sessionStorage.setItem("group_id", JSON.parse(response.data)["group_id"]);
      user["group_id"] = this.propsGroupID;
      var new_user = JSON.stringify(user);
      const url = "http://46.18.25.97:8050/users/organizer";
      this.sendRequest(url, "POST", new_user, "organizer", "insert");
      this.page = "rest";
      this.pageInd = "urest";
    });
  },
  beforeUnmount() {
    window.removeEventListener("beforeunload", this.beforeWindowUnload);
    sessionStorage.clear();
    sessionStorage.removeItem("userPreferenceList");
    sessionStorage.removeItem("group_id");
    sessionStorage.removeItem("location");
    sessionStorage.removeItem("group_members_status");
    sessionStorage.removeItem("Selected");
    sessionStorage.removeItem("remember");
    sessionStorage.removeItem("menuList");
    sessionStorage.removeItem("menuValidity");
    sessionStorage.removeItem("MenuSize");
    sessionStorage.removeItem("menuSizeValidity");
    sessionStorage.clear();
  },
  created() {
    window.addEventListener("beforeunload", this.beforeWindowUnload);
  },
};
</script>
<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@1,300&family=Shadows+Into+Light&display=swap");
.header {
  position: absolute;
  top: 30;
  width: 100%;
}
.front {
  background-image: url("../assets/back3.jpg");
  -webkit-background-size: 100%;
  -moz-background-size: 100%;
  -o-background-size: 100%;
  background-size: 100%;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
}
.individual {
  background-image: url("../assets/individual.jpg");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  opacity: 80%;
}
.individual:active {
  opacity: 100%;
}

.group {
  background-image: url("../assets/group.jpg");
  background-repeat: no-repeat;
  background-size: 100% 100%;
  opacity: 80%;
}
.group:active {
  opacity: 100%;
}
.textwhite {
  color: white;
  font-size: x-large;
  font-family: "Roboto", sans-serif;
  font-family: "Shadows Into Light", cursive;
  font-weight: bold;
}
.textblack {
  color: black;
  font-size: x-large;
  font-family: "Roboto", sans-serif;
  font-family: "Shadows Into Light", cursive;
  font-weight: bold;
}
.size {
  font-size: 1rem;
}
.scroll {
  margin-top: 50px;
}
.q-tab {
  cursor: default;
}
.q-header {
  cursor: pointer;
}
</style>
