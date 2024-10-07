<template>
  <div class="kale">
    <div :class="['sidebar', { collapsed: isCollapsed, animate: animateElements }]" role="navigation">
      <button class="toggle-btn" @click="toggleSidebar">
        <i class="fas fa-bars" aria-hidden="true"></i>
        <span v-if="isCollapsed" class="sr-only">Expand</span>
        <span v-else class="sr-only">Collapse</span>
      </button>
      <h1 class="sstyle" v-if="!isCollapsed">Sidebar</h1>
      <ul v-if="!isCollapsed">
        <li><router-link :to="`/udashboard/${id}/${username}`">Dashboard</router-link></li>
        <li><router-link :to="`/mybooks/${id}`">My Books</router-link></li>
      </ul>
    </div>
    <div class="top" :class="{ animate: animateElements }">
      <div class="logo" :class="{ animate: animateElements }">
        <img :src="logo" alt="Logo">
      </div>
      <h1 class="welcome-message">Borrow Books</h1>
      
    </div>

    <div class="main-content" :class="{ animate: animateElements }" role="main">

      <div class="bbinfo-blocks">
        <div class="bbinfo-block" :class="{ animate: animateElements }">
          <h3>Library Books</h3>
          <input type="text" v-model="bookSearch" placeholder="Search books...">
          <ul>
            <li v-for="book in filteredBooks" :key="book.id">
              <h4>{{ book.name }}</h4>
              <p>Author: {{ book.author }}</p>
              <p>{{ book.content }}</p>
              <div class="button-group">
                <button class="edit-button" v-if="!book.is_borrowed && !isBookBorrowed(book.id)" @click="borrowBook(book.id)">Borrow</button>
                <button class="delete-button" v-else-if="isBookBorrowed(book.id)" @click="returnBook(book.id)">Return</button>
                <div v-if="message" class="alert" :class="{'alert-success': success, 'alert-danger': !success}">
                    {{ message }}
                </div>
              </div>
            </li>
          </ul>
        </div>
        <div class="bbinfo-block" :class="{ animate: animateElements }">
          <h3>Sections</h3>
          <input type="text" v-model="sectionSearch" placeholder="Search sections...">
          <ul>
            <li v-for="section in filteredSections" :key="section.id">
              <h4>{{ section.name }}:</h4>
              <p>Number of books: {{ section.book_count }}</p>
              <ul>
                <li v-for="book in section.books" :key="book.id">
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
  name: 'BorrowBooks',
  props: ['id', 'username'],
  data() {
    return {
      isCollapsed: false,
      logo: require('@/assets/logo.jpg'),
      animateElements: false,
      books: [],
      sections: [],
      bookSearch: '',
      sectionSearch: '',
      message: '', // Added message here
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
    logout() {
      console.log('Logging out...');
    },
    deleteAccount() {
      console.log('Deleting account...');
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
    async borrowBook(bookId) {
      console.log('Attempting to borrow book with ID:', bookId); // Debug log
      if (!bookId) {
        console.error('Invalid book ID');
        return;
      }
      try {
        const response = await axios.post(`http://localhost:5000/borrow/${bookId}`, {
          consumer_id: this.id,
          consumer_name: this.username,
          filename: ''
        });
        console.log('Borrow response:', response.data);

        this.message = 'Borrow Book request sent successfully';
        this.success = true; 

        this.fetchBooks();  
      } catch (error) {
        console.error('Error borrowing book:', error);
        this.message = error.response.data.message; // Correct error message assignment
        this.success = false;
      }
    },
    async returnBook(bookId) {
      try {
        await axios.post('http://localhost:5000/return', {
          id: bookId,
          user_id: this.id
        });
        this.fetchBooks();
      } catch (error) {
        console.error('Error returning book:', error);
      }
    },
    isBookBorrowed(bookId) {
      return this.books.some(book => book.id === bookId && book.is_borrowed && book.is_approved);
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
.bbinfo-blocks {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    flex-wrap: nowrap;
    flex-direction: row;

  
}

.bbinfo-block {
  max-height: 444px;
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

.bbinfo-block.animate {
  opacity: 1;
  transform: translateY(0);
}
.bbinfo-block input {
  width: 100%;
  margin-bottom: 10px;
}

.bbinfo-block ul {
  
  padding: 0;
}

.bbinfo-block li {
    margin-left: 50px;
    margin-bottom: 10px;
}
.bbinfo-block h3 {
  margin-top: 0;
}

.bbinfo-block input {
  width: 90%;
  padding: 8px;
  margin-bottom: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

</style>
