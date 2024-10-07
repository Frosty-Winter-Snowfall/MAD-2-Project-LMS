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
      <h1 class="welcome-message">Add Books to Sections</h1>
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">
      <div class="signup-form" role="form" aria-label="AddSections Form">
        <div class="header">
          <h1>Add Books to Sections</h1>
        </div>
        <form @submit.prevent="submitbooktosections" enctype="multipart/form-data">
          <div class="form-group">
            <label for="book_id">Book:</label>
            <select v-model="book_id" class="form-control" id="book_id" required>
              <option v-for="book in books" :key="book.id" :value="book.id">
                {{ book.name }} by {{ book.author }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="section_id">Section:</label>
            <select v-model="section_id" class="form-control" id="section_id" required>
              <option v-for="section in sections" :key="section.id" :value="section.id">
                {{ section.name }}
              </option>
            </select>
          </div>
          <button type="submit" class="btn btn-primary">Add Book to Section</button>
        </form>
        <div v-if="message" class="alert" :class="success ? 'alert-success' : 'alert-danger'" role="alert">
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
  name: 'AddBookstos',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      book_id: null,
      section_id: null,
      books: [],
      sections: [],
      message: '',
      success: false
    };
  },

  mounted() {
    this.triggerAnimation();
    this.fetchBooks();
    this.fetchSections();
  },
  methods: {
    toggleSidebar() {
      this.isCollapsed = !this.isCollapsed;
    },
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    async fetchBooks() {
      try {
        const response = await axios.get('http://localhost:5000/books');
        this.books = response.data;
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async fetchSections() {
      try {
        const response = await axios.get('http://localhost:5000/sections');
        this.sections = response.data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    async submitbooktosections() {
      try {
        const formData = new FormData();
        formData.append('book_id', this.book_id);
        formData.append('section_id', this.section_id);

        const response = await axios.post('http://localhost:5000/addbooktosection', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Book to Section uploaded successfully:', response.data);
        this.message = response.data.message;
        this.success = true;
        this.clearForm();
      } catch (error) {
        console.error('Error adding book to section:', error);
        this.message = 'Error adding book to section.';
        this.success = false;
      }
    },
    clearForm() {
      this.book_id = null;
      this.section_id = null;
    }
  }
};
</script>

<style>
.form-group {
  margin-bottom: 15px;
}

</style>
