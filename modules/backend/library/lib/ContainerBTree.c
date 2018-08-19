
#include <stdio.h>
#include <stdlib.h>
#include "../header/Container.h"
#include "BTree.h"

MAP2CHECK_CONTAINER new_container(enum Container_Type type) {
  MAP2CHECK_CONTAINER container;
  container.size = 0;
  B_TREE* btree = malloc(sizeof(B_TREE));
  switch (container.type) {
    case LIST_LOG_CONTAINER:
      *btree = B_TREE_CREATE("listlog.map2check.bin");
      break;
    case ALLOCATION_LOG_CONTAINER:
      *btree = B_TREE_CREATE("allocationlog.map2check.bin");
      break;
    case NONDET_LOG_CONTAINER:
      *btree = B_TREE_CREATE("nondetlog.map2check.bin");
      break;
    case HEAP_LOG_CONTAINER:
      *btree = B_TREE_CREATE("heaplog.map2check.bin");
      break;
    case TRACKBB_LOG_CONTAINER:
      *btree = B_TREE_CREATE("trackbblog.map2check.bin");
      break;
  }

  container.values = btree;
  container.type = type;
  return container;
}

Bool free_container(MAP2CHECK_CONTAINER* container) {
  switch (container->type) {
    case LIST_LOG_CONTAINER:
      // TODO (rafa.sa.xp@gmail.com) for some reason this causes a segmentation
      // fault
      // system("rm -rf listlog.map2check.bin");
      break;
    case ALLOCATION_LOG_CONTAINER:
      system("rm -rf allocationlog.map2check.bin");
      break;
    case NONDET_LOG_CONTAINER:
      system("rm -rf nondetlog.map2check.bin");
      break;
    case HEAP_LOG_CONTAINER:
      system("rm -rf heaplog.map2check.bin");
      break;
    case TRACKBB_LOG_CONTAINER:
      system("rm -rf trackbblog.map2check.bin");
      break;
  }
  B_TREE_FREE((B_TREE*)container->values);
  free(container->values);
  return TRUE;
}

Bool append_element(MAP2CHECK_CONTAINER* container, void* row) {
  B_TREE_ROW btRow;
  btRow.index = container->size;
  container->size += 1;

  switch (container->type) {
    case LIST_LOG_CONTAINER:
      btRow.value.listLog = *((LIST_LOG_ROW*)row);
      break;
    case ALLOCATION_LOG_CONTAINER:
      btRow.value.allocationLog = *((MEMORY_ALLOCATIONS_ROW*)row);
      break;
    case NONDET_LOG_CONTAINER:
      btRow.value.kleeLog = *((NONDET_CALL*)row);
      break;
    case HEAP_LOG_CONTAINER:
      btRow.value.heapLog = *((MEMORY_HEAP_ROW*)row);
      break;
    case TRACKBB_LOG_CONTAINER:
      btRow.value.trackBBLog = *((TRACK_BB_ROW*)row);
      break;
  }
  B_TREE_INSERT(container->values, &btRow);
  return TRUE;
}

void* get_element_at(unsigned index, MAP2CHECK_CONTAINER container) {
  if (index >= container.size) {
    return NULL;
  }

  B_TREE_ROW* row = B_TREE_SEARCH(container.values, index);
  return &row->value;
}
