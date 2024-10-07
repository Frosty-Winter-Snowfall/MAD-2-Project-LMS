<template>
  <div class="libd">
    <div :class="['sidebar', { collapsed: isCollapsed, animate: animateElements }]" role="navigation">
      <button class="toggle-btn" @click="toggleSidebar">
        <i class="fas fa-bars" aria-hidden="true"></i>
        <span v-if="isCollapsed" class="sr-only">Expand</span>
        <span v-else class="sr-only">Collapse</span>
      </button>
      <h1 class="sstyle" v-if="!isCollapsed">Sidebar</h1>
      <ul v-if="!isCollapsed">
        <li><router-link :to="`/ldashboard/${id}/${username}`">Dashboard</router-link></li>
        <li><router-link :to="{ path: '/bookmanagement', query: { id: id, username: username } }">Book Management</router-link></li>
        <li><router-link :to="{ path: '/sectionmanagement', query: { id: id, username: username } }">Section Management</router-link></li>
        <li><router-link :to="{ path: '/usermanagement', query: { id: id, username: username } }">User Management</router-link></li>
      </ul>
    </div>
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Edit Sections</h1>
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="signup-form" role="form" aria-label="EditSection Form">
        <div class="header">
          <h1>Edit Sections</h1>
        </div>
        <form @submit.prevent="submitEditedSection" enctype="multipart/form-data">
          <div class="mb-3">
            <label for="name" class="form-label">Name of Section:</label>
            <input type="text" id="name" v-model="newName" class="form-control" placeholder="Enter the new name of the Section">
          </div>
          <div class="mb-3">
            <label for="content" class="form-label">Description:</label>
            <input type="text" id="content" v-model="newContent" class="form-control" placeholder="Give a brief description">
          </div>
          <button type="submit" class="btn btn-primary">Save Changes</button>
        </form>
        <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
          {{ message }}
        </div>
      </div>
    </div>

    <div class="footer" :class="{ animate: animateElements }">
        <p>Contact Me: 22f3000877@ds.study.iitm.ac.in | Happy Reading!</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'EditSections',
  props: ['sectionId', 'id', 'username'],
  data() {
    return {
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      newName: '',
      newContent: '',
      message: '',
      success: false
    };
  },

  mounted() {
    console.log('sectionId:', this.sectionId);
    this.triggerAnimation();
    this.fetchSectionDetails();
  },

  methods: {
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },

    async fetchSectionDetails() {
      try {
        const response = await axios.get(`http://localhost:5000/section/${this.sectionId}`);
        this.newName = response.data.name;
        this.newContent = response.data.content;
      } catch (error) {
        console.error('Error fetching section details:', error);
      }
    },

    async submitEditedSection() {
      try {
        const formData = new FormData();
        formData.append('new_name', this.newName);
        formData.append('new_content', this.newContent);

        const response = await axios.post(`http://localhost:5000/editsections/${this.sectionId}`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Section edited successfully:', response.data);
        this.message = response.data.message;
        this.success = true;
        this.clearForm();
      } catch (error) {
        console.error('Error editing section:', error);
        this.message = 'Error editing section.';
        this.success = false;
      }
    },

    clearForm() {
      this.newName = '';
      this.newContent = '';
    }
  }
};
</script>

<style>
.alert-success {
  color: green;
}

.alert-danger {
  color: red;
}
</style>
