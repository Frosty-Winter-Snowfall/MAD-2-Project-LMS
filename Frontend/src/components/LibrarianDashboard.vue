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
       <li><router-link :to="{ path: '/bookmanagement', query: { id: id, username: username } }">Book Management</router-link></li>
        <li><router-link :to="{ path: '/sectionmanagement', query: { id: id, username: username } }">Section Management</router-link></li>
        <li><router-link :to="{ path: '/usermanagement', query: { id: id, username: username } }">User Management</router-link></li>
      </ul>
    </div>
    <div class="top"  :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Welcome {{ username }}</h1>
      <div class="account">
        <button class="account-btn" aria-haspopup="true" aria-expanded="false">
          <i class="bi bi-backpack-fill"></i>
        </button>
        <div class="account-actions" role="menu">
          <form @submit.prevent="logout">
            <button type="submit" class="edit-button" role="menuitem">Logout</button>
          </form>
        </div>
      </div>
    </div>


    <div class="main-content" :class="{ animate: animateElements }" role="main">
    <div class="lwelcome-card" :class="{ animate: animateElements }">
        <h2>Welcome Back, {{ username }} ! What will you be doing today?</h2>
        
        <ul>
          <li><router-link :to="{ path: '/addbooks', query: { id: id, username: username } }">Add new books</router-link></li>
          <li><router-link :to="{ path: '/addsections', query: { id: id, username: username } }">Add new sections</router-link></li>
          <li><router-link :to="{ path: '/viewfeedback', query: { id: id, username: username } }">View Ratings</router-link></li>
          <li><router-link :to="{ path: '/statistics', query: { id: id, username: username } }">View Statistics</router-link></li>
        </ul>
        <button class="export-csv-btn" @click="triggerCsvExport">Export Books as CSV</button>
      </div>
      <div class="linfo-blocks">
        <div class="linfo-block" :class="{ animate: animateElements }">
        <h3>Library Books</h3>
          <input type="text" v-model="bookSearch" placeholder="Search books...">
          <ul>
            <li v-for="book in filteredBooks" :key="book.id">
              <h4>{{ book.name }}</h4>
              <p>Author: {{ book.author }}</p>
              <p>{{ book.content }}</p>
            </li>
          </ul>
        </div>
        <div class="linfo-block" :class="{ animate: animateElements }">
          <h3>Sections</h3>
          <input type="text" v-model="sectionSearch" placeholder="Search sections...">
          <ul>
            <li v-for="section in filteredSections" :key="section.id">
              <h4>{{ section.name }} :</h4>
              <p>Number of books: {{ section.book_count }}</p>
              <ul>
                <li v-for="book in section.books" :key="book.name">
                  <p>Book: {{ book.name }} by {{ book.author }}</p>
                </li>
              </ul>
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
  name: 'LibrarianDashboard',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      books: [],
      sections: [],
      bookSearch: '',
      sectionSearch: ''
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
    async logout() {
    try {
      await axios.post('http://localhost:5000/logout', {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      localStorage.removeItem('token');
      this.$router.push('/'); 
    } catch (error) {
      console.error('Error logging out:', error);
    }
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
        const response = await axios.get('http://localhost:5000//sections');
        this.sections = response.data;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    },
    async triggerCsvExport() {
      try {
        await axios.post('http://localhost:5000/trigger_csv_export', {}, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        alert('CSV export has been triggered. You will receive an email once it is done.');
      } catch (error) {
        console.error('Error triggering CSV export:', error);
      }
    }
  },
  computed: {
    filteredBooks() {
      return this.books.filter(book => 
        book.name.toLowerCase().includes(this.bookSearch.toLowerCase()) ||
        book.author.toLowerCase().includes(this.bookSearch.toLowerCase())
      );
    },
    filteredSections() {
      return this.sections.filter(section => 
        section.name.toLowerCase().includes(this.sectionSearch.toLowerCase())
      );
    }
  }
};
</script>

<style>


.animate {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 1s ease-out, transform 1s ease-out;
}

.lwelcome-card {
  background-color: #f0f0f0b0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  margin-bottom: 20px;
  width: calc(100% - 40px); /* Full width within its container */
  transition: all 1s ease-out;
    opacity: 0;
    transform: translateY(20px);
}

.lwelcome-card.animate {
  opacity: 1;
  transform: translateY(0);
}

.linfo-blocks {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: nowrap;
    flex-direction: row;

  
}

.linfo-block {
  max-height: 150px;
  width: 50%; 
  margin: 10px 0;
  background: #f0f0f0b0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  transition: all 1s ease-out;
  opacity: 0;
  transform: translateY(20px);
  overflow-y: auto;
}

.linfo-block.animate {
  opacity: 1;
  transform: translateY(0);
}
.linfo-block input {
  width: 100%;
  margin-bottom: 10px;
}

.linfo-block ul {
  
  padding: 0;
}

.linfo-block li {
    margin-left: 50px;
    margin-bottom: 10px;
}
.linfo-block h3 {
  margin-top: 0;
}

.linfo-block input {
  width: 90%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.main-content {
  padding: 20px;
  flex: 1;
  overflow: auto;
  display: flex;
  flex-direction: column;
}
  
.export-csv-btn {
  background-color: #ff5e96;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
}

.export-csv-btn:hover {
  background-color: #55d0ff;
}

</style>
