library(magrittr)

# Convert string to bit representation
char_to_bit <- function(s) {
  s %>%
    charToRaw() %>%
    rawToBits()
}


# Convert bit representation to string
bit_to_char <- function(b) {
  b %>%
    packBits(type = "raw") %>%
    rawToChar()
}


# Random bit stream of desired length
random_bit_stream <- function(size, prob_1 = 0.5) {
  sample(x = as.raw(c(0x00, 0x01)),
         size = size,
         replace = TRUE,
         prob = c(1.0 - prob_1, prob_1))
}


# Transmission over binary symmetric channel
transmit <- function(b, f) {
  # Probability f of flipping
  noise <- random_bit_stream(size = length(b),
                             prob_1 = f)
  xor(b, noise)
}


H2 <- function(f) {
  dplyr::if_else(
    f == 0 | f == 1,
    0.0,
    -f * log2(f) - (1.0 - f) * log2(1.0 - f)
  )
}


capacity <- function(f) {
  1.0 - H2(f)
}


# Fraction of bits different between
error_rate <- function(b1, b2) {
  mean(b1 != b2)
}


# Repetition codes ----
rep_code_encode <- function(b, N) {
  checkmate::assert_count(N)
  checkmate::assert_raw(b)
  rep(b, each = N)
}


Mode <- function(x) {
  u <- unique(x)
  tab <- x %>%
    match(u) %>%
    tabulate()
  # Sample a single value in case of multiple modes
  u %>%
    `[`(tab == max(tab)) %>%
    sample(1)
}


split_every <- function(x, N, pad = NA) {
  lx <- length(x)
  # First pad on right to ensure correct length
  pad_length <- ceiling(lx / N) * N - lx
  x <- c(x, rep(pad, pad_length))
  if (length(x)/N > 1) {
    reps <- x %>%
      seq_along() %>% 
      cut(length(x)/N, labels = FALSE)
    x %>%
      split(reps) %>%
      unname()
  } else {
    x
  }
}


rep_code_decode <- function(b, N) {
  b %>%
    split_every(N) %>%
    purrr::map(Mode) %>%
    unlist(use.names = FALSE)
}


is_odd <- function(x) {
  (x %% 2L) != 0L
}


rep_code_error_proba <- function(f, N) {
  dplyr::if_else(rep(is_odd(N), each = length(f)),
                 true = stats::pbinom(N %/% 2, N, f, lower.tail = FALSE),
                 false = NULL)
}