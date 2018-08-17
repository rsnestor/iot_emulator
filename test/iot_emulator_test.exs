defmodule IotEmulatorTest do
  use ExUnit.Case
  doctest IotEmulator

  test "greets the world" do
    assert IotEmulator.hello() == :world
  end
end
