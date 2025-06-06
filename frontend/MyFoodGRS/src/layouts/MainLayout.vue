<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title> MyFood </q-toolbar-title>
      </q-toolbar>
    </q-header>

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
    <q-layout
      view="lHh lpr lFf"
      container
      style="height: 120px"
      class="shadow-2 rounded-borders"
    >
      <q-header elevated>
        <q-toolbar> </q-toolbar>

        <q-tabs v-model="tab">
          <q-tab
            name="Restuarants"
            label="Restuarants"
            icon="restaurantmenu"
            @click="determinePage('rest')"
          />
          <q-tab
            name="Group"
            label="Group"
            icon="group"
            @click="determinePage('group')"
          />
          <q-tab
            name="Bookmark"
            label="Bookmark"
            icon="favorite"
            @click="determinePage('book')"
          />
        </q-tabs>
      </q-header>
    </q-layout>
    <GroupPage v-if="page === 'group'" :groupInfo="groupInfo"></GroupPage>
    <RestaurantPage
      v-if="page === 'rest' && propsGroupID > 0"
      :groupInfo="groupInfo"
      :groupId="propsGroupID"
    ></RestaurantPage>
    <BookmarkPage
      v-if="page === 'book' && propsGroupID > 0"
      :groupInfo="groupInfo"
      :groupId="propsGroupID"
    ></BookmarkPage>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from "vue";
// import EssentialLink from "components/EssentialLink.vue";
import GroupPage from "components/GroupPage.vue";
import BookmarkPage from "components/BookmarkPage.vue";
import RestaurantPage from "components/RestaurantPage.vue";
import UserPage from "components/UserPage.vue";
import UserBookmarkPage from "components/UserBookmarkPage.vue";
import UserRestaurantPage from "components/UserRestaurantPage.vue";
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
    // EssentialLink,
    GroupPage,
    RestaurantPage,
    BookmarkPage,
  },

  setup() {
    const leftDrawerOpen = ref(false);

    return {
      propsGroupID: -1,
      tab: ref("mails"),
      essentialLinks: linksList,
      leftDrawerOpen,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value;
      },
    };
  },
  data() {
    return {
      page: "",
      groupInfo: {},
      membersName: {},
      default_member_info: {},
    };
  },
  methods: {
    determinePage(pageToChange) {
      this.page = pageToChange;
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
            sessionStorage.setItem(role, temp_user_id);
            sessionStorage.setItem(role_name, first_name);
            this.groupInfo[temp_user_id] = [role, first_name];
            var temp_element_to_add = {};
            temp_element_to_add["id"] = temp_user_id;
            temp_element_to_add["name"] = first_name;
            temp_element_to_add["show"] = true;
            this.membersName[role] = temp_element_to_add;
            this.default_member_info = this.membersName;
            return temp_user_id;
          });
      }
    },
  },
  beforeCreate() {
    sessionStorage.clear();
    sessionStorage.removeItem("group_id");
    sessionStorage.removeItem("location");
    sessionStorage.removeItem("group_members_status");
    sessionStorage.removeItem("Selected");
  },
  mounted() {
    sessionStorage.setItem("location", false);
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
    axios.get("http://46.18.25.97:8050/group").then((response) => {
      this.propsGroupID = JSON.parse(response.data)["group_id"];
      sessionStorage.setItem("group_id", JSON.parse(response.data)["group_id"]);
      user["group_id"] = this.propsGroupID;
      var new_user = JSON.stringify(user);
      const url = "http://46.18.25.97:8050/users/organizer";
      this.sendRequest(url, "POST", new_user, "organizer", "insert");
      this.page = "group";
    });
  },
  beforeUnmount() {
    sessionStorage.clear();
    sessionStorage.removeItem("group_id");
    sessionStorage.removeItem("location");
    sessionStorage.removeItem("group_members_status");
    sessionStorage.removeItem("Selected");
  },
};
</script>
<style scoped>
.header {
  position: absolute;
  top: 30;
  width: 100%;
}
</style>
