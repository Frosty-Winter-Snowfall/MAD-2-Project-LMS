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
        <li><router-link :to="{ path: '/usermanagement', query: { id: id, username: username } }">User Management</router-link></li>
      </ul>
    </div>
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Manage Sections</h1>
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="lwelcome-card" :class="{ animate: animateElements }">
        <h2>Welcome Back, {{ username }}!</h2>
        <p>Let's manage Sections together!</p>
        <ul>
          <li><router-link :to="{ path: '/addbookstos', query: { id: id, username: username } }">Add Books to Sections</router-link></li>
          <li><router-link :to="{ path: '/removebooksfroms', query: { id: id, username: username } }">Remove Books from Sections</router-link></li>
        </ul>
      </div>
       <div class="sinfo-blocks" :class="{ animate: animateElements }">
        <div class="sinfo-block" :class="{ animate: animateElements }">
          <h3>Edit Sections</h3>
          <ul>
            <li v-for="section in sections" :key="section.id">
        <h4>{{ section.name }}</h4>
        <p>{{section.content}}</p>
        <div class="button-group">
        <button class="edit-button" @click="navigateToEditSections(section.id)">Edit</button>
        <div class="button-gap"></div>
        <button class="delete-button" @click="deleteSection(section.id)">Delete</button>
        <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
        {{ message }}
      </div>
        </div>
            </li>
          </ul>
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
  name: 'SectionManagement',
  props: ['id', 'username','sectionId'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      sections: [],
      sectionToEdit: null,
      newSectionName: '',
      message: '',
      success:false
    };
  },
  mounted() {
    this.triggerAnimation();
    this.fetchSections();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    async fetchSections() {
      try {
        const response = await axios.get('http://localhost:5000/section');
        this.sections = response.data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    
    
    async deleteSection(sectionId) {
      try {
        const response=await axios.post(`http://localhost:5000/deletesection/${sectionId}`);
        this.message = 'Section deleted successfully!';
        this.fetchSections();
        this.message = response.data.message;
        this.success = true;
      } catch (error) {
        console.error('Error deleting section:', error);
        this.message = 'Error deleting section.';
        this.success=false;
      }

    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    navigateToEditSections(sectionId) {
    this.$router.push({
      path: `/editsections/${sectionId}`,
      query: { id: this.id, username: this.username } });
    }
  }
};
</script>


<style>
/* Styles for the sinfo-blocks container */
.sinfo-blocks {
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 1s ease-out;
  opacity: 0;
  transform: translateY(20px);
  
}

/* Styles for the sinfo-block */
.sinfo-block {
  background-color: #f0f0f0b0;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin: 10px;
  width: 500px;
  transition: all 1s ease-out;
  opacity: 0;
  transform: translateY(20px);
  height: 150px; /* Fixed height for the sinfo-blocks container */
  overflow-y: auto; /* Enable vertical scrolling */
}

.sinfo-blocks.animate {
  opacity: 1;
  transform: translateY(0);
}

.sinfo-block.animate {
  opacity: 1;
  transform: translateY(0);
}

/* Styles for the button-group container */
.button-group {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Styles for the button-gap */
.button-gap {
  width: 10px; /* Adjust the width of the gap */
}

/* Styles for the edit-button */
.edit-button {
  background-color: #ff5e96; /* Pink color */
  color: #fff;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.edit-button:hover {
  background-color: #55D0FF; /* Darker shade of pink on hover */
}

/* Styles for the delete-button */
.delete-button {
  z-index:1000;
  background-color: #e90f0f;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.delete-button:hover {
  background-color: #55D0FF;
}

.alert-success {
  color: green;
}

.alert-danger {
  color: red;
}
</style>