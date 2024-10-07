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
      <h1 class="welcome-message">Remove Book from Section</h1>
    </div>
    <div class="main-content" :class="{ animate: animateElements }" role="main">
    <div class="remove-book-section">
      <h2>Remove Book from Section</h2>
      <form @submit.prevent="removeBookFromSection">
        <div class="form-group">
          <label for="sectionId">Select Section:</label>
          <select v-model="selectedSection" id="sectionId" class="form-control" @change="fetchBooksInSection" required>
            <option v-for="section in sections" :key="section.id" :value="section.id">
              {{ section.name }}
            </option>
          </select>
        </div>
        <div class="form-group" v-if="books.length">
          <label for="bookId">Select Book:</label>
          <select v-model="selectedBook" id="bookId" class="form-control" required>
            <option v-for="book in books" :key="book.book_id" :value="book.book_id">
              {{ book.book_name }}
            </option>
          </select>
        </div>
        <button type="submit" class="btn btn-danger" :disabled="!selectedBook">Remove Book</button>
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
  name: 'RemoveBookSection',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      selectedSection: null,
      selectedBook: null,
      sections: [],
      books: [],
      message: '',
      success: false
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
    triggerAnimation() {
      setTimeout(() => {
        this.animateElements = true;
      }, 100);
    },
    async fetchSections() {
      try {
        const response = await axios.get('http://localhost:5000/section'); // Ensure endpoint is correct
        this.sections = response.data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    async fetchBooksInSection() {
      try {
        const response = await axios.get(`http://localhost:5000/books_in_section/${this.selectedSection}`);
        this.books = response.data;
        this.selectedBook = null; // Reset selected book when section changes
      } catch (error) {
        console.error('Error fetching books:', error);
      }
    },
    async removeBookFromSection() {
      try {
        const response = await axios.delete(`http://localhost:5000/removebookfromsection/${this.selectedBook}`);
        this.message = response.data.message;
        this.success = true;
        this.books = this.books.filter(book => book.book_id !== this.selectedBook); // Remove book from list
        this.selectedBook = null; // Reset selected book
      } catch (error) {
        console.error('Error removing book from section:', error);
        this.message = error.response.data.message || 'Error removing book from section.';
        this.success = false;
      }
    }
  }
};
</script>

<style>
.remove-book-section {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.form-group {
  margin-bottom: 15px;
}
.form-control {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
}
.btn {
  display: inline-block;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
  text-decoration: none;
  outline: none;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 8px;
}
.btn-danger {
  background-color: #dc3545;
}
.alert {
  margin-top: 20px;
  padding: 10px;
  border-radius: 5px;
}
.alert-success {
  background-color: #d4edda;
  color: #155724;
}
.alert-danger {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
