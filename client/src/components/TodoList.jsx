import React from 'react'
import TodoItem from './TodoItem'

export default class TodoList extends React.Component {
  getItems() {
    if (this.props.todos) {
      return this.props.todos.filter(
        (item) => this.props.filter === 'all' || item.get('status') === this.props.filter
      );
    }
    return [];
  }
  isCompleted(item) {
    return item.get('status') === 'completed';
  }
  render() {
    return <section className="body">
      <ul className="todos">
        {this.getItems().map(item =>
          <TodoItem key={item.get('text')}
                    text={item.get('text')}
                    id={item.get('id')}
                    isCompleted={this.isCompleted(item)}
                    toggleComplete={this.props.toggleComplete}/>
        )}
      </ul>
    </section>
  }
};
